from datetime import datetime, timedelta

import json

from app.models.mll_cfg import obtener_cfg_general, actualizar_en_ejecucion
from app.models.mll_cfg_bbdd import obtener_conexion_bbdd_origen
from app.config.db_mallorquina import get_db_connection_sqlserver, get_db_connection_mysql, close_connection_mysql
from app.services.auxiliares.sendgrid_service import enviar_email

from app.utils.mis_excepciones import MiException
from app.utils.utilidades import graba_log, imprime
from app.utils.functions import select_mysql
from app.utils.InfoTransaccion import InfoTransaccion


# Constantes globales
ID_NUBE = 1   # ID de BBDD de la nube (infosoft) que es donde están todos los datos de CAJA



#----------------------------------------------------------------------------------------
# Este proceso se encarga de recorrer todas las tiendas/BBDD y entidades para hacer el arqueo de caja       
# para ello:
#   - Recorre todas las entidades cuya tienda/bb tenga cierre_caja=S
#   - Para cada entidad, busca en arque_ciego de BBDD La Mallorquina, todos los datos para la fecha elegida y que tenga una forma de pago que se tenga en cuanta en el arqueo de caja tpv_formas_de_cobro.activo_arqueo = 1
#       - Los datos son  entidad, id_cierre, id_cobro, puesto, serie, importe
#   - Con los datos de arque_ciego, se consulta en Caja de SQLSERVER, los datos de la entidad, id_cierre, id_cobro, puesto, serie, importe
#   - Se graba el arqueo de caja en la BBDD de La Mallorquina
#   - Se actualiza la fecha de último cierre de la entidad
#----------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion) -> list:
    funcion = "arqueo_caja.proceso"
    param.debug="Inicio"
    resultado = []
    conn_mysql = None # para que no de error en el finally
    conn_sqlserver = None
    cursor_mysql = None # para que no de error en el finally
    dias = param.parametros[0]


    try:
        config = obtener_cfg_general(param)
        
        if  not config.get("ID", False): 
            param.registrar_error(ret_txt= f"No se han encontrado datos de configuración: {config['En_Ejecucion']}", debug=f"{funcion}.config-ID")
            raise MiException(param = param)
            
        if config["En_Ejecucion"]:
            param.registrar_error(ret_txt="El proceso ya está en ejecución.", debug=f"{funcion}.config.en_ejecucion")
            raise MiException(param = param)

        # Buscamos la conexión a MySQL porque es donde vamos a grabar y donde vamos a buscar datos auxiliares del arqueo de caja
        param.debug="actualizar_en_ejecucion"
        actualizar_en_ejecucion(param, 1)
        param.debug = "get_db_connection_mysql"
        conn_mysql = get_db_connection_mysql()
        # ----------------------------------------------------------------------------------------------------------------------------------

        # Buscamos la conexión que necesitamos para esta bbdd origen SQLSERVER en la NUBe que es con la que vamos a hacer el arqueo de caja
        param.debug = "Buscamos la conexión que necesitamos para esta bbdd origen"
        bbdd_config = obtener_conexion_bbdd_origen(conn_mysql, ID_NUBE)
        param.debug = "conectamos con esta bbdd origen"
        conn_sqlserver = get_db_connection_sqlserver(bbdd_config)
        # ----------------------------------------------------------------------------------------------------------------------------------

        # for fecha in fechas:
        param.debug = "Select"
        lista_entidades = select_mysql(param=param, conn_mysql=conn_mysql, query="""SELECT e.ID, e.nombre, e.id_bbdd, e.stIdEnt, ifnull(e.ultimo_cierre, '2025-01-01') as ultimo_cierre
                                                                                      FROM mll_cfg_entidades e
                                                                                     inner join mll_cfg_bbdd bd on e.id_bbdd = bd.id
                                                                                     WHERE bd.cierre_caja = 'S'""")
                   
        for x in range(1, dias+1):
            cursor_mysql = conn_mysql.cursor(dictionary=True)

            for entidad in lista_entidades:
                fecha = datetime.strptime(entidad["ultimo_cierre"], "%Y-%m-%d") + timedelta(days=x)
                imprime([f"Procesando TIENDA: {entidad}", fecha, entidad["ultimo_cierre"], x], "-")
                resultado_dict = consultar_y_grabar(param, conn_mysql, conn_sqlserver, entidad["ID"], entidad["stIdEnt"], fecha)
                resultado.extend(resultado_dict)
                conn_mysql.commit()

                if resultado_dict:  # es muy raro no que se tengan datos, algo ha pasado, nos quedamos que el último cierre 
                    param.debug = "update"
                    cursor_mysql.execute("UPDATE mll_cfg_entidades SET ultimo_cierre = %s WHERE ID = %s",
                                        (fecha, entidad["ID"],)
                                        )
        
            conn_mysql.commit()        

        actualizar_en_ejecucion(param, 0)

        return resultado if resultado else [f"No se han encontrado datos desde el {datetime.strptime(entidad['ultimo_cierre'], '%Y-%m-%d') + timedelta(days=1)} al {datetime.strptime(entidad['ultimo_cierre'], '%Y-%m-%d') + timedelta(days=dias+1)}"]


    except MiException as e:
        param.error_sistema(e=e, debug="Sincroniza.Proceso.MiExcepcion")
        raise e
    
    except Exception as e:
        param.error_sistema(e=e, debug="Sincroniza.proceso.Exception")
        raise e
        
    finally:
        close_connection_mysql(conn_mysql, cursor_mysql)
        if conn_sqlserver:
            conn_sqlserver.close()

        enviar_email(config["Lista_emails"],
                     "Proceso finalizado",
                     "El proceso de sincronización ha terminado."
        )


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def consultar_y_grabar(param: InfoTransaccion, conn_mysql, conn_sqlserver, id_entidad, stIdEnt, fecha) -> dict:
    resultado = []
    param.debug = "Inicio"

    try:
        # fecha_mas_1 = (datetime.strptime(fecha, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        fecha_mas_1 = (fecha + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        query = """SELECT ac.stIdEnt, ac.fecha_hora,  ac.id_cobro, ac.descripcion, ac.importe, cc.Id_Cierre, pt.Serie
                     FROM tpv_arqueo_ciego ac
                    inner join tpv_cierres_de_caja cc     on ac.id_apertura = cc.Id_Cierre and ac.stIdEnt = cc.stIdEnt
                    inner join tpv_puestos_facturacion pt on cc.Id_Puesto = pt.Id_Puesto   and ac.stIdEnt = pt.stIdEnt
                    inner join tpv_formas_de_cobro fc     on ac.Id_Cobro = fc.Id_Cobro	   and ac.stIdEnt = fc.stIdEnt
                    WHERE Fecha_hora >= %s 
                      AND Fecha_hora < %s
                      AND fc.activo_arqueo = 1
                      -- AND ac.importe != 0
                      AND ac.stIdEnt = %s
                    ORDER by ac.stIdEnt, ac.fecha_hora, ac.id_cobro, cc.Id_Cierre, pt.Serie"""  # Vamos a coger todas las tiendas del dia
        
        # recuperamos los IDs de cierre para un día, ya que en caja puede haber movimientos para un cierre de dos fechas diferentes
        cursor_mysql = conn_mysql.cursor(dictionary=True)
        cursor_mysql.execute(query, (fecha, fecha_mas_1, stIdEnt))
        ids_cierre = cursor_mysql.fetchall()

        # imprime([query, len(ids_cierre), (fecha, fecha_mas_1, stIdEnt)], "* query", 2)
        
        for cierre in ids_cierre:
            # Leer datos desde SQL Server
            cursor_sqlserver = conn_sqlserver.cursor()
            param.debug = "Ejecución select 2"
            select_query = """SELECT Ca.stIdEnt, Ca.[Id Apertura Puesto Cobro] as ID_Apertura,
                                        FORMAT(Ca.[Fecha], 'dd/MM/yyyy') as Fecha,
                                        Ca.[Id Cobro] as ID_Cobro,
                                        Ca.[Descripcion Cobro] as Medio_Cobro,
                                        Ca.[Serie Puesto Facturacion] as ID_Puesto,
                                        sum(Ca.[Entrada]-Ca.[Salida]) as Importe,
                                        count(*) as Operaciones
                                    FROM Caja Ca
                                WHERE Ca.[Id Apertura Puesto Cobro]  = ?
                                        AND Ca.[Serie Puesto Facturacion] = ?
                                        AND Ca.[Id Cobro] = ?
                                        AND Ca.stIdEnt = ?
                                group by Ca.stIdEnt,    Ca.[Id Apertura Puesto Cobro], FORMAT(Ca.[Fecha], 'dd/MM/yyyy'),
                                            Ca.[Id Cobro], Ca.[Descripcion Cobro],        Ca.[Serie Puesto Facturacion]"""

            cursor_sqlserver.execute(select_query, (cierre["Id_Cierre"], cierre["Serie"], cierre["id_cobro"],cierre['stIdEnt'],))
            datos = cursor_sqlserver.fetchall()
            cursor_sqlserver.close()

            # imprime([select_query, len(datos), (cierre["Id_Cierre"], cierre["Serie"], cierre["id_cobro"],cierre['stIdEnt'])], "* select_query", 2)

            param.debug = "Llamada a Grabar"
            resultado.extend(grabar(param, conn_mysql, id_entidad, datos, fecha, (cierre["Id_Cierre"], cierre["Serie"], cierre["id_cobro"],cierre['stIdEnt'],cierre["importe"],cierre['fecha_hora'])))

        return resultado


    except Exception as e:
        param.error_sistema(e=e, debug="consultar_y_grabar.Exception")
        raise 

    
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def grabar(param: InfoTransaccion, conn_mysql, id_entidad, datos, fecha, cierre) -> dict:
    param.debug = "Inicio"
    resultado = []
    ventas_registros = 0
    total_ventas = 0
    total_operaciones = 0
    medios_pago_registros = 0

    try: 
        cursor_mysql = conn_mysql.cursor()
        # Agrupar resultados por tienda, puesto y apertura
        ventas_diarias = {}


        for row in datos:
            id_puesto = row.ID_Puesto
            id_apertura = row.ID_Apertura
            fecha = row.Fecha

            # Clave única para agrupación
            key = (id_entidad, id_puesto, id_apertura)

            if key not in ventas_diarias:
                ventas_diarias[key] = {
                    "id_entidad": id_entidad,
                    "id_tpv": id_puesto,
                    "fecha": fecha,
                    "ventas": 0,
                    "operaciones": 0,
                    "detalles": [],
                }

            ventas_diarias[key]["ventas"] += row.Importe
            ventas_diarias[key]["operaciones"] += row.Operaciones
            ventas_diarias[key]["detalles"].append(row)
            

        orden = 1 # porque en la primera alteración quiero que sea 0
        # Insertar en mll_rec_ventas_diarias
        for idx, (key, data) in enumerate(ventas_diarias.items()):
            orden = orden ^ 1  # Alternar entre 0 y 1
            param.debug = "insert mll_rec_ventas_diarias"
            ID_Apertura = key[2]
            # esto igual es mejor meterlo en un array todo y aquí buscar en el array
            id_mae_tpv = 0  # busca_tvp(param, conn_mysql, data["id_entidad"],  data["id_tpv"])

            insert_diarias = """INSERT INTO mll_rec_ventas_diarias (id_entidad, Serie, id_mae_tpv, fecha, imp_arqueo_ciego, ventas, operaciones, cierre_tpv_id, cierre_tpv_desc)
                                                            VALUES (%s, %s, %s, STR_TO_DATE(%s, '%d/%m/%Y'), %s, %s, %s, %s, %s)"""
            # imprime([insert_diarias, 
            #          (data["id_entidad"],data["id_tpv"],id_mae_tpv,data["fecha"],cierre[4],data["ventas"],data["operaciones"],ID_Apertura,cierre[4],)
            #         ], 
            #         "* DATOS ", 2)
            cursor_mysql.execute( insert_diarias,
                                  (data["id_entidad"],
                                   data["id_tpv"],
                                   id_mae_tpv,
                                   data["fecha"],
                                   cierre[4],
                                   data["ventas"],
                                   data["operaciones"],
                                   ID_Apertura,
                                   cierre[5],
                                  )
                                )
            id_ventas_diarias = cursor_mysql.lastrowid  # Obtener el ID insertado

            ventas_registros  += cursor_mysql.rowcount
            total_ventas += data["ventas"]
            total_operaciones += data["operaciones"]

            # Insertar en mll_rec_ventas_medio_pago
            for detalle in data["detalles"]:
                if detalle.Importe != 0 or detalle.Operaciones != 0:
                    insert_medio_pago = """INSERT INTO mll_rec_ventas_medio_pago (id_ventas_diarias, id_medios_pago, ventas, operaciones)
                                                                          VALUES (%s, %s, %s, %s)"""
                    cursor_mysql.execute(insert_medio_pago,(id_ventas_diarias,
                                                            detalle.ID_Cobro,
                                                            detalle.Importe,
                                                            detalle.Operaciones,
                                                           )
                    )
                    medios_pago_registros  += cursor_mysql.rowcount

        if ventas_registros != 0:
            resultado = [f"para el {fecha} y entidad {id_entidad}: se han creado {ventas_registros} regsitros de venta, con un total de {total_ventas}€ ({cierre[4]}) para {total_operaciones} operaciones. En Medios de pago se han creado {medios_pago_registros} registros"]

        return resultado

    except Exception as e:
        param.error_sistema(e=e, debug="grabar.Exception")
        raise 


# #----------------------------------------------------------------------------------------
# #----------------------------------------------------------------------------------------
# def busca_tvp(param: InfoTransaccion, conn_mysql, id_tienda,  id_tpv) -> int:
#     resultado = 0
#     param.debug = "busca_tvp Inicio"

#     try: 
#         cursor_mysql = conn_mysql.cursor(dictionary=True)
#         query = f"""SELECT pf.id_mae_tpv FROM tpv_puestos_facturacion pf
#                      where pf.serie={id_tpv}
#                        and pf.Origen_BBDD = {id_tienda}
#                  """
#         param.debug="execute del cursor"
#         cursor_mysql.execute(query)
#         datos = cursor_mysql.fetchall()
#         if datos:
#             # imprime([type(datos), datos], "=")
#             param.debug= "en el FOR, solo debería tener un registro"
#             resultado = datos[0]['id_mae_tpv']


#     except Exception as e:
#         param.error_sistema(e=e, debug="busca_tvp.Exception")
 

#     finally:
#         return resultado

    


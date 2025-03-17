from datetime import datetime, timedelta
from decimal import Decimal
import re

from app.utils.utilidades import graba_log, imprime
from app.config.db_mallorquina import get_db_connection_sqlserver, close_connection_sqlserver

from app.utils.InfoTransaccion import InfoTransaccion
#from app.utils.mis_excepciones import MiException

TAMAÑO_LOTE: int = 500
SALTO: int = 500


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion, conn_mysql, entidad, tabla, bbdd_config, campos, tabla_config) -> list:
    param.debug="General_1"
    conn_sqlserver = None

    try:
        campos_origen = [campo['Nombre'] for campo in campos]
        campos_destino = [campo['Nombre_Destino'] for campo in campos]
        # imprime([f"entidad: {entidad}",  
        #          f"Tabla: {tabla}",  
        #          f"bbdd_config: {bbdd_config}",  
        #          f"Campos Origen: {campos_origen}",    
        #          f"Campos Destino: {campos_destino}",  
        #          f"Campos placeholders: {', '.join(['%s'] * len(campos_destino))}", 
        #          f"tabla_config: {tabla_config}"], 
        #          f"*...¿Que parametros?...", 2)     
        # ------------------------------------------------------------------------------------------------------------------------
        # Validaciones
        # para [Facturas Cabecera] ULT_VALOR debe tener la fecha de siguiente carga y los dias a cargar de una tirada, 
        # por ejemplo: "2025-01-01, 1" que indica que la próxima carga desde empezar en el día 01/01/2025 y se debe cargar un dia.
        # ------------------------------------------------------------------------------------------------------------------------
        valores = tabla['ult_valor'].replace(" ", "").split(",")  
        desde = valores[0]  # fecha en formato yyyy-mm-dd
        dias = int(valores[1]) if len(valores) > 1 else 1  # Si falta, asigna 1

        if desde:
            desde = datetime.strptime(f"{desde} 00:00:00", "%Y-%m-%d %H:%M:%S")
        else:
            raise ValueError("No está parametrizado el ult_valor de Facturas Cabeceras")
        hasta = desde + timedelta(days=1)
        # ------------------------------------------------------------------------------------------------------------------------

        param.debug = "conn origen"
        # conextamos con esta bbdd origen
        conn_sqlserver = get_db_connection_sqlserver(bbdd_config)

        # Hacer un bucle por fechas pedidas
        empieza = datetime.now()
        # ------------------------------------------------------------------------------------------------------------------------
        registros = obtener_y_grabar(param, conn_sqlserver, conn_mysql, entidad, tabla, desde, hasta, dias, campos_origen, campos_destino, tabla_config)
        # ------------------------------------------------------------------------------------------------------------------------
        imprime([f"Segundos: {(datetime.now()-empieza).total_seconds()}",
                 f"Registros: {len(registros)} - desde {empieza} a {datetime.now()}"], 
                 "*", 2)
        
        return registros

    except Exception as e:
        param.error_sistema(e=e, debug="General_1.proceso")
        raise e

    finally:
        # param.debug = f"cierra conexión sqlserver: {param.debug}"
        close_connection_sqlserver(conn_sqlserver, None)

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def obtener_y_grabar(param: InfoTransaccion, conn_sqlserver, conn_mysql, entidad, tabla, desde, hasta, dias, campos_origen, campos_destino, tabla_config) -> list:
    param.debug="Obtener_datos_origen"
    stIdEnt = entidad["stIdEnt"]
    valor_max = None
    insertados = 0
    actualizados = 0
    registros = [valor_max, insertados, actualizados]

    

    try:
        # Leer datos desde SQL Server
        param.debug = "crear cursor"
        cursor_sqlserver = conn_sqlserver.cursor()
       
        # --------------------------------------------------------------------------------
        param.debug = "Inicio 1733" 
        vez = 1
        while vez <= dias:
            pos = 0
            while True:
                param.debug = f"Ejecución select {vez}"
                cadena_select = ', '.join(campos_origen)
                match = re.search(r"t\..*?\]", tabla_config['where'])
                if match:
                    orden = match.group()  # Captura toda la coincidencia
                else:
                    raise ValueError("No tenemos ORDEN")

                select_query = f"""SELECT {cadena_select.replace("{0}", f"{entidad['ID']}  as id_entidad" )} 
                                     FROM {tabla_config['Tabla_Origen']} t
                                    WHERE t.stIdEnt = ? 
                                      AND {tabla_config['where']} --  where debe llevar un formato con dos parametros tipo: "t.[Fecha] >= ?  AND t.[Fecha] < ?"  o "? = ?"
                                    ORDER BY {orden} -- t.[Fecha_Hora]
                                    OFFSET ? ROWS            -- Salta x filas
                                    FETCH NEXT {SALTO} ROWS ONLY; -- Toma las siguientes SALTO lineas
                                """
                if pos == 0:
                    imprime([select_query, stIdEnt, desde, hasta, pos], "* -- QUERY -- ", 2)

                cursor_sqlserver.execute(select_query, (stIdEnt, desde, hasta, pos)) 
                datos = cursor_sqlserver.fetchall()
                if len(datos) == 0:   # hemos terminado
                    break

                # -----------------------------------------------------------------------------------
                param.debug = "Llamada a Grabar"
                valor_max, insertados, actualizados = grabar_datos(param, conn_mysql, entidad['id_bbdd'], datos, hasta, campos_destino, tabla_config)
                # -----------------------------------------------------------------------------------

                registros[0]  = valor_max
                registros[1] += insertados
                registros[2] += actualizados
                pos          += SALTO

            # FIN DIA
            # actualizamos control y COMMIT
            cursor_mysql = conn_mysql.cursor()
            param.debug = "Execute fec_ult_act"
            cursor_mysql.execute("""UPDATE mll_cfg_tablas_entidades
                                    SET Fecha_Ultima_Actualizacion = %s, 
                                        ult_valor = COALESCE(%s, ult_valor)
                                    WHERE ID = %s""",
                                (datetime.now(), f'{hasta.strftime("%Y-%m-%d")}, 1', tabla["ID"]) # lo hacemos con el hasta porque hemos cargado < HASTA
                                )
            conn_mysql.commit()
        
            desde = hasta
            hasta = desde + timedelta(days=1)
            vez += 1

        cursor_sqlserver.close()
        # ---------------------------------------------------------------

        return registros

    except Exception as e:
        param.error_sistema(e=e, debug="Ganeral_1.Obtener_y_grabar")
        raise 
        

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def grabar_datos(param: InfoTransaccion, conn_mysql, id_BBDD, datos, hasta, campos_destino, tabla_config) -> list:
    param.debug="facturas_cabecera"
    cursor_mysql = None # para que no de error en el finally
    valor_max = hasta
    insertados = 0
    actualizados = 0

    try:
        cadena_select = ', '.join(campos_destino) + ", Origen_BBDD"
        cadena_placeholders = ', '.join(['%s'] * (len(campos_destino)+1))
        insert_query = f"INSERT INTO {tabla_config['Tabla_Destino']}   ({cadena_select})  VALUES({cadena_placeholders});"

        datos_aux = [convertir_datos(fila) for fila in datos]
        datos_convertidos = [tupla + (id_BBDD,) for tupla in datos_aux]

        # Validación para ver si todos los registros y tienen el mismo número de campos.....
        # for i in range(0, len(datos_convertidos), 1):
        #     lote = [tuple(registro) for registro in datos_convertidos[i:i + 1]]  # Convertir a tuplas extrayendo una porción de la lista
        #     if len(lote[0]) != 44:
        #         imprime([f"lote: {lote[0]}"], f"*...Lote: {i}-{len(lote[0])}...", 2)
        #         raise ValueError(f"Error en el lote {i} de {len(lote[0])} elementos")

        with conn_mysql.cursor() as cursor_mysql:
            leidos = len(datos_convertidos)
            param.debug = f"Bucle1 de {0} a {TAMAÑO_LOTE} de {leidos}"
            for i in range(0, leidos, TAMAÑO_LOTE):
                param.debug = f"Bucle2 de {i} a {i+TAMAÑO_LOTE} de {leidos}"
                lote = datos_convertidos[i:i + TAMAÑO_LOTE]  # Extraer una porción de la lista

                lote = [tuple(registro) for registro in datos_convertidos[i:i + TAMAÑO_LOTE]]  # Convertir a tuplas extrayendo una porción de la lista
                # imprime([f"type(lote): {type(lote)}", f"type(lote[0]): {type(lote[0])}"], f"-", 2)
                # for x, fila in enumerate(lote):
                #     print(f"Fila {x}: {type(fila)} - {len(fila)} elementos")
                #     for j, valor in enumerate(fila):
                #         print(f"  🟢 Pos {j}: {type(valor)} - <{valor}>")
                #     break    
                cursor_mysql.executemany(insert_query, lote)  # Insertar el lote
                insertados += cursor_mysql.rowcount
       
        return [valor_max, insertados, actualizados]

    except Exception as e:
        param.error_sistema(e=e, debug="General_1.Grabar_Datos.Excepcion")
        raise 


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def convertir_datos(registro):
    return tuple(
        val.strftime("%Y-%m-%d %H:%M:%S") if isinstance(val, datetime) else  # Convierte datetime
        float(val)                        if isinstance(val, Decimal) else  # Convierte Decimal a float
        int(val)                          if isinstance(val, bool) else  # Convierte booleanos a 1 o 0
        # None                              if val == None else  # Reemplaza "" con None
        None                              if val == "" else  # Reemplaza "" con None
        val  # Dejar los demás valores igual
        for val in registro
    )
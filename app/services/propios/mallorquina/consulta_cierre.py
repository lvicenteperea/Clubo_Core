from datetime import datetime, date
import json

# Para trabajar con Excel PANDA
import pandas as pd

# Para trabajar con Excel OPENPYXL
from openpyxl import Workbook

from app.models.mll_cfg import obtener_cfg_general
from app.config.db_mallorquina import get_db_connection_mysql, close_connection_mysql
from app.services.auxiliares.sendgrid_service import enviar_email

from app.utils.utilidades import graba_log, imprime
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings
from app.utils.mis_excepciones import MiException

RUTA = f"{settings.RUTA_DATOS}cierre_caja/"

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion) -> list:
    param.debug="Inicio"
    resultado = []
    datos = []
    config = obtener_cfg_general(param)

    imprime([param], "*  ver parametros", 2)

    fecha = param.parametros[0] # el primer  atributo de InfArqueoCajaRequest
    entidad = param.parametros[1]  # el segundo atributo de InfArqueoCajaRequest


    print(fecha, entidad)
    param.debug = "get_db_connection_mysql"
    try:
        conn_mysql = get_db_connection_mysql()
        cursor_mysql = conn_mysql.cursor(dictionary=True)

        param.debug = "Select"
        query = "SELECT * FROM mll_cfg_entidades WHERE id = %s AND activo='S'"
        cursor_mysql.execute(query, (entidad,))

        lista_entidades = cursor_mysql.fetchall()  # Solo debería haber una

        # imprime([lista_entidades, type(lista_entidades), len(lista_entidades), fecha, entidad], "*  LISTA_ENTIDADES", 2)

        for entidad in lista_entidades:
            imprime([f"Procesando TIENDA: {entidad['ID']}-{entidad['Nombre']}. De la BBDD: {entidad['id_bbdd']}"], "-")
            datos.extend(consultar(param, entidad["ID"], conn_mysql, fecha))

        if datos:
            # imprime ([datos, type(datos), len(datos)], "*  DATOS", 2)
            return datos
        else:
            return ["No se ha generado información  porque no hay datos"]



    except MiException as e:
        param.error_sistema(e=e, debug="Consulta_Cierre.Proceso.MiExcepcion")
        raise e
    except Exception as e:
        param.error_sistema(e=e, debug="Consulta_Cierre.Proceso.Excepcion")
        raise e # HTTPException(status_code=500, detail=e)


    finally:
        close_connection_mysql(conn_mysql, cursor_mysql)

        enviar_email(config["Lista_emails"],
                     "Proceso finalizado",
                     ["El proceso de informes de Consulta cierres ha terminado."]
        )


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def consultar(param: InfoTransaccion, id_entidad, conn_mysql, fecha) -> list:
    resultado = []
    param.debug="Inicio"

    param.debug = "get_db_connection_mysql"
    try:
        cursor_mysql = conn_mysql.cursor(dictionary=True)

        param.debug = "Select"
        query = f"""SELECT 
                        vd.id_entidad,
                        t.nombre Tienda,
                        vd.serie,
                        pf.descripcion Nombre_TPV,
                        vd.fecha,
                        vd.cierre_tpv_id,
                        vd.cierre_tpv_desc,
                        vmp.id_medios_pago,
                        mp.nombre Nombre_MdP,
                        sum(vd.imp_arqueo_ciego) AS total_arqueo_ciego,
                        SUM(vmp.ventas) AS total_ventas,
                        SUM(vmp.operaciones) AS total_operaciones
                    FROM mll_rec_ventas_diarias vd
                        JOIN  mll_rec_ventas_medio_pago vmp ON vd.id = vmp.id_ventas_diarias
                    LEFT JOIN mll_cfg_entidades t         ON vd.id_entidad = t.id
                    LEFT JOIN tpv_puestos_facturacion pf ON vd.serie = pf.serie and vd.id_entidad = pf.id_entidad
                    LEFT JOIN mll_mae_medios_pago mp ON vmp.id_medios_pago = mp.id
                    where vd.id_entidad={id_entidad}
                      and vd.fecha = STR_TO_DATE('{fecha}', '%Y-%m-%d')
                    GROUP BY 
                        vd.id_entidad,
                        t.nombre,
                        vd.serie,
                        pf.descripcion,
                        vd.fecha,
                        vd.cierre_tpv_id,
                        vd.cierre_tpv_desc,
                        vmp.id_medios_pago,
                        mp.nombre
                 """

        param.debug="execute del cursor"
        cursor_mysql.execute(query)
        datos = cursor_mysql.fetchall()

        param.debug= "en el FOR"
        for row in datos:
            resultado.append(row)

        return resultado

    except Exception as e:
        param.error_sistema(e=e, debug="consultar.Exception")
        raise 

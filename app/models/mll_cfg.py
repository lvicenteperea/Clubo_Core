from app.config.db_mallorquina import get_db_connection_mysql, close_connection_mysql
from app.utils.mis_excepciones import MiException
from app.utils.InfoTransaccion import InfoTransaccion
from app.utils.utilidades import graba_log, imprime

#----------------------------------------------------------------------------------------
def obtener_cfg_general(param: InfoTransaccion):
    
    try:
        param.debug ='Inicio'
        conn = get_db_connection_mysql()

        param.debug ='cursor'
        cursor = conn.cursor(dictionary=True)

        param.debug ='select'
        cursor.execute("SELECT * FROM mll_cfg LIMIT 1")

        param.debug ='fetch'
        config = cursor.fetchone()

        if not config.get("ID", False):
            param.registrar_error(ret_txt = f"No se han encontrado datos de configuración", debug="obtener_cfg_general.config-ID")
            raise MiException(param = param)

        return config

    except Exception as e:
        param.error_sistema(e=e, debug="Excepción mll_cfg.obtener_cfg_general")
        raise

    finally:
        close_connection_mysql(conn, cursor)

#----------------------------------------------------------------------------------------
def actualizar_en_ejecucion(param: InfoTransaccion, estado: int):

    try:
        conn = get_db_connection_mysql()

        cursor = conn.cursor()
        cursor.execute("UPDATE mll_cfg SET En_Ejecucion = %s", (estado,))
        conn.commit()

        close_connection_mysql(conn, cursor)

    except Exception as e:
        param.error_sistema(e=e, debug="Excepción mll_cfg.obtener_cfg_general")
        raise

    finally:
        close_connection_mysql(conn, cursor)

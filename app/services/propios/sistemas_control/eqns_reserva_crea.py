from app.utils.utilidades import graba_log, imprime
from app.config.db_clubo import get_db_connection_mysql, close_connection_mysql
from app.utils.InfoTransaccion import InfoTransaccion

from app.services.externos.sistemas_control.equinsa import crea_reserva

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion) -> list:
    resultado = []
    param.debug = "proceso"
    # punto_venta = param.parametros[1]


    try:
        # Llammar a proceso de reservas de Clubo para ver si es posible, formatear datos, guardar información, logs....

        # Llamar a servicio externos de equinsa (lo que hacen las inserciones en los Sistemas de Control)

        imprime(["✅", param], "* Servicio 'eqns_reserva_crea' realizado")

        return resultado or []

    except Exception as e:
        param.error_sistema(e=e, debug="proceso.Exception")
        raise 

    finally:
        param.debug = "finaliza"
    

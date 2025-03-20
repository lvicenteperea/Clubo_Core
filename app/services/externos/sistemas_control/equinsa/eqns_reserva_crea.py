from app.config.servicios_equinsa import EquinsaService

from app.models.reservas import crea_reserva

from app.utils.utilidades import graba_log, imprime
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion) -> list:
    resultado = []
    param.debug = "proceso"
    # punto_venta = param.parametros[1]
    equinsa = EquinsaService(carpark_id="1237")
    param.parametros.append(equinsa)


    try:
        # Llammar a proceso de reservas de Clubo para ver si es posible, formatear datos, guardar información, logs....
        resultado = crea_reserva(param)

        # Llamada al servicio de Equinsa para crear la reserva
        # datos_equinsa = equinsa.execute_sql_1command(sql_query)
        # resultado = datos_equinsa["rows"]

        return resultado or []

    except Exception as e:
        param.error_sistema(e=e, debug="proceso.Exception")
        raise 

    finally:
        param.debug = "finaliza"
    

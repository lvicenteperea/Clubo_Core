from app.utils.utilidades import graba_log, imprime
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def crea_reserva(param: InfoTransaccion) -> list:

    imprime([param.parametros], "*")
    return []
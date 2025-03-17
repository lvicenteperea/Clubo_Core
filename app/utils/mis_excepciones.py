from app.utils.utilidades import imprime
from app.utils.InfoTransaccion import InfoTransaccion

class MiException(Exception):
    def __init__(self, param: InfoTransaccion = None, detail: str = "", status_code: int = 0):
        self.status_code = status_code
        self.detail = detail
        self.param = param if param else InfoTransaccion()
        imprime([f"Codigo - Msg - Param: <{self.status_code}> - <{self.detail}> - <{self.param}>"], "=   MiException   ")



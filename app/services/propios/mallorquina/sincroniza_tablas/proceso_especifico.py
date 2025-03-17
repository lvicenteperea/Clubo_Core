import importlib

from app.utils.utilidades import graba_log, imprime
from app.utils.InfoTransaccion import InfoTransaccion

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion, conn_mysql, entidad, tabla, bbdd_config, campos, tabla_config):
    param.debug="proceso_especifico"
    valor_max = None

    try:
        mi_metodo = tabla_config["proceso_carga"]
        mi_modulo = importlib.import_module("app.services.mallorquina.sincroniza_tablas."+mi_metodo)
        func = getattr(mi_modulo, "proceso", None)  # Obtener la función desde otro módulo

        # imprime([func, tabla_config['Tabla_Destino'], entidad, tabla, bbdd_config, tabla_config], "=   --- proceso_especifico ---   ", 2)
        if func:
            resultado = func(param, conn_mysql, entidad, tabla, bbdd_config, campos, tabla_config)  # Ejecutar la función
        else:
            param.debug = f"no se encontró el módulo {mi_metodo} para cargar la tabla {tabla_config['Tabla_Destino']} con la tabla {tabla_config['Tabla_Origen']}."
            raise ValueError(f"El módulo {mi_metodo} no se encontró en 'app.services.mallorquina.sincroniza_tablas'.")

        return resultado.extend([None]) # añadimos un None al final para que coincida con el retorno de proceso_general y es OK

    except Exception as e:
        param.error_sistema(e=e, debug="PRoceso_especifico.Exception")
        raise e

import logging
import logging.config
import traceback

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# esto sería con fichero de inicialización
try:
    print("inicializa logging")
    logging.config.fileConfig('app/logging.ini')
except Exception as e:
    print(f"Error configuring logging: {e}")

# Obtén los loggers
# logger = logging.getLogger('app_logger')
app_logger = logging.getLogger('app_logger')
time_logger = logging.getLogger('time_logger')


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
def graba_log(mi_mensaje:dict, origen: str, e, logger = app_logger):
    try:
        loc = "no disponible"

        if isinstance(e, BaseException): # Comprueba si es una excepción
            tb = traceback.extract_tb(e.__traceback__)
            archivo, linea, funcion, texto_err = tb[-1]
            loc = f'{texto_err.replace("-", "_")} - {archivo.replace("-", "_")} - {linea} - {funcion}'

        # Intentar obtener un código de error
        if hasattr(e, 'errno'):  # Excepciones del sistema
            err_num = e.errno
        elif hasattr(e, 'args') and len(e.args) > 0:  # Excepciones genéricas con args
            err_num = e.args[0]
        else:
            err_num = 0

        logger.error(f"MI ERROR: {origen}: {mi_mensaje} - ERROR: {err_num} - {str(e)} - LOCALIZACION: {loc})")

    except Exception as e:
        imprime(["Error en graba_log:", e], relleno="*")
        return

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
def graba_log_info(mensaje, logger = time_logger):

    logger.info(mensaje)

    for handler in logger.handlers:
        print(f"Handler: {handler}")
        handler.flush()

#------------------------------------------------------------------------------------------------
"""
Esta función es una ayuda para el desarrollo para hacer print de información
    Función que imprime textos con líneas de relleno al inicio y al final.

    Parámetros:
    - textos: lista de textos a imprimir.
    - relleno: carácter que se repetirá en la línea de relleno.
    - modo: 1 (por defecto) imprime todos los textos en la misma línea;
            otro valor imprime cada texto en una línea distinta.

             ✅
             ❌
             🟢
             🔍
"""
#------------------------------------------------------------------------------------------------
def imprime(textos: list, relleno: str = " ", modo: int = 1):
    titulo = None
    long = 80

    if not relleno or relleno.strip() == "":
        relleno = " "

    linea_relleno = relleno[0] * long

    if len(relleno) > 1:
        titulo = "  " + relleno[1:] + "  "
        index_medio = len(linea_relleno) // 2
        print(linea_relleno[:index_medio] + titulo + linea_relleno[index_medio:])
        linea_relleno = linea_relleno + (relleno[0] * len(titulo))
    else:
        print(linea_relleno)

    if len(textos) > 0:
        # Imprimir los textos
        if modo == 1:
            resultado = "<" + "> - <".join(str(elemento) for elemento in textos) + ">"
            print(resultado)
        else:
            for texto in textos:  # Cada texto en una línea separada
                print(texto)
    else:
        print("Lista vacia")

    print(linea_relleno)


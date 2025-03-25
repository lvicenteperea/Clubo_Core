from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import json
import traceback
from datetime import datetime
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


from app.utils.mis_excepciones import MiException
from app.utils.InfoTransaccion import InfoTransaccion
from app.utils.utilidades import graba_log, imprime

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
async def mi_exception_handler(request: Request, exc: MiException):
    if exc.status_code >= 0: 
        status_code = 200
        mensaje = exc.detail
    elif exc.status_code > -90: # -1, -2.... no son errores graves de cortar el programa
        status_code = 401
        mensaje = exc.detail
    else:                       # -90.... no deberían salir por aquí, pero serían para cortar el programa.
        status_code = 525
        imprime([f"ERROR CRÍTICO: {exc.detail}"], "=   mi_exception_handler   ")
        mensaje = "Contacte con su administrador"
    
    return JSONResponse(
        status_code=status_code,
        content={"status_code": exc.status_code, "message": mensaje}
    )

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    imprime([f"ERROR GENERAL: {str(exc)}"], "=   validation_exception_handler   ")
    errors = exc.errors()
    detalles = []

    for err in errors:
        detalles.append({
            "campo": err.get("loc", []),
            "mensaje": err.get("msg"),
            "tipo": err.get("type")
        })

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Error de validación", "detalles": detalles}
    )





# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
async def generic_exception_handler(request: Request, exc: Exception):
    loc = "no disponible"
    imprime([f"ERROR GENERAL: {str(exc)}"], "=   generic_exception_handler   ")

    # ---------------------------------------------------------------------------------------------------------------------------
    param = InfoTransaccion(id_App=1, user="Vamos a ver1", ret_code=-1, ret_txt=str(exc), parametros=[])

    if isinstance(exc, BaseException): # Comprueba si es una excepción
        tb = traceback.extract_tb(exc.__traceback__)
        archivo, linea, funcion, texto_err = tb[-1]
        loc = f'{texto_err.replace("-", "_")} - {archivo.replace("-", "_")} - {linea} - {funcion}'

    graba_log(param, f"generic_exception_handler: {loc}", exc)

    imprime([f"HTTP ERROR: {exc}", 
             f"📌 URL: {request.url}",
             f"📌 Método: {request.method}",
             f"📌 Headers: {dict(request.headers)}",
             #f"📌 Body: {await request.body()}",  # Para leer el cuerpo de la solicitud
             #f"📌 Detalles del error: {exc.detail}",
             f"📌 Localización: {loc}"
            ], "=   http_exception_handler   ", 2)
    # ---------------------------------------------------------------------------------------------------------------------------

    return JSONResponse(
        status_code=500,
        content={"status_code": 500, 
                 "message": f"Error general. contacte con su administrador ({datetime.now().strftime('%Y%m%d%H%M%S')})"
                }
    )

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
async def http_exception_handler(request: Request, exc: HTTPException):
    loc = "no disponible"
    imprime([f"ERROR HTTP: {str(exc)}"], "=   http_exception_handler   ")

    # ---------------------------------------------------------------------------------------------------------------------------
    param = InfoTransaccion(id_App=1, user="Vamos a ver", ret_code=-1, ret_txt="pues el RET_TXT", parametros=[])

    if isinstance(exc, BaseException): # Comprueba si es una excepción
        tb = traceback.extract_tb(exc.__traceback__)
        archivo, linea, funcion, texto_err = tb[-1]
        loc = f'{texto_err.replace("-", "_")} - {archivo.replace("-", "_")} - {linea} - {funcion}'

    graba_log(param, f"{funcion}.http_exception_handler", exc)


    imprime([f"HTTP ERROR: {exc}", 
             f"📌 URL: {request.url}",
             f"📌 Método: {request.method}",
             f"📌 Headers: {dict(request.headers)}",
             f"📌 Body: {await request.body()}",  # Para leer el cuerpo de la solicitud
             f"📌 Detalles del error: {exc.detail}",
             f"📌 Localización: {loc}"
            ], "=   http_exception_handler   ", 2)
    # ---------------------------------------------------------------------------------------------------------------------------

    return JSONResponse(
        status_code=exc.status_code,
        content={"status_code": exc.status_code, 
                 "message": f"Error general. contacte con su administrador ({datetime.now().strftime('%Y%m%d%H%M%S')})"
                }
    )

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
async def json_decode_error_handler(request: Request, exc: json.JSONDecodeError):
    imprime([f"JSON Decode Error: {exc.msg}"], "=   json_decode_error_handler   ")

    return JSONResponse(
        status_code=400,
        content={"status_code": 400, "message": "Error al decodificar JSON"}
    )

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
async def type_error_handler(request: Request, exc: TypeError):
    imprime([f"Type Error: {str(exc)}"], "=   type_error_handler   ")

    return JSONResponse(
        status_code=422,
        content={"status_code": 422, "message": "Error de tipo en la solicitud"}
    )

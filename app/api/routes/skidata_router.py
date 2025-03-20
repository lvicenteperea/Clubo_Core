from fastapi import APIRouter, HTTPException, Body, Request, Depends, File, UploadFile, Form
from datetime import datetime

from app.services.externos.sistemas_control.skidata import skd_carga_tablas, skd_crea_tablas

from app.config.db_clubo import get_db_connection_sqlserver, close_connection_sqlserver

from app.config.settings import settings
from app.utils.functions import control_usuario
from app.utils.utilidades import imprime

from app.utils.mis_excepciones import MiException
from app.utils.InfoTransaccion import InfoTransaccion, ParamRequest

router = APIRouter()

# -----------------------------------------------
# Función para manejar excepciones de manera estándar
# -----------------------------------------------
def manejar_excepciones(e: Exception, param: InfoTransaccion, endpoint: str):
    if isinstance(e, MiException):
        return None
    elif isinstance(e, HTTPException):
        param.error_sistema(e=e, debug=f"{endpoint}.HTTP_Exception")
        raise e
    else:
        param.error_sistema(e=e, debug=f"{endpoint}.Exception")
        raise e


# -----------------------------------------------
# Función común para procesar requests
# -----------------------------------------------
async def procesar_request(
    request: Request, body_params: ParamRequest, servicio, endpoint: str
) -> InfoTransaccion:
    tiempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Validación y construcción de parámetros
        param = InfoTransaccion.from_request(body_params)
        if not control_usuario(param, request):
            return param

        # Ejecución del servicio correspondiente
        resultado = servicio.proceso(param=param)

        # Construcción de respuesta
        param.debug = f"Retornando: {type(resultado)}"
        param.resultados = resultado or []
        return param


    except Exception as e:
        manejar_excepciones(e, param, endpoint)
        return param  # si no es MiException, se retorna el param
    
    finally:
        imprime([tiempo, datetime.now().strftime('%Y-%m-%d %H:%M:%S')], "* FIN TIEMPOS *")







# -----------------------------------------------
# Endpoints individuales
# -----------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
class ApkConsultasRequest(ParamRequest):
    query: str = ""

@router.post("/apk_consultas", response_model=InfoTransaccion,
             summary="🔄 Crealiza consultas sobre un aparcamiento de equinsa",
             description="""........................................\n
                                - ✅ **Requiere autenticación**
                                - ✅ **Recibe un `id_App` y un `user`** para identificar al peticionario
                                - ✅ **Retorna `status` y `message` indicando error**
                         """,
             response_description="""📌 En caso de éxito retorna una clase InfoTransaccion y en resultados una lista con los ficheros generados:\n
                                  """
            )
async def apk_consultas(request: Request,
                        body_params: ApkConsultasRequest = Body(...)
):

    tiempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        # --------------------------------------------------------------------------------
        # Validaciones y construcción Básica
        # --------------------------------------------------------------------------------
        param = InfoTransaccion.from_request(body_params)

        control_usuario(param, request)

        # --------------------------------------------------------------------------------
        # Servicio
        # --------------------------------------------------------------------------------
        bbdd_config = {"host": "192.168.17.99", "port": "1433", "user": "onlineuser", "database": "PARK_DB", "password": "Not4LocalUsers!"} # obtener_conexion_bbdd_origen(conn_mysql, ID_NUBE)
        param.debug = "conectamos con esta bbdd origen"
        conn_sqlserver = get_db_connection_sqlserver(bbdd_config)
        cursor_sqlserver = conn_sqlserver.cursor()

        query = param.parametros[0] # """SELECT table_name FROM INFORMATION_SCHEMA.TABLES where table_catalog = ?"""
        
        cursor_sqlserver.execute(query)
        # resultado = cursor_sqlserver.fetchall()
        resultado = [list(row) for row in cursor_sqlserver.fetchall()]
        close_connection_sqlserver(conn_sqlserver,  cursor_sqlserver)
        

        param.debug = f"Retornando un lista: {type(resultado)}"
        param.resultados = resultado or []
        return param

    except Exception as e:
        # manejar_excepciones(e, param, "apk_consultas")
        imprime(["Mensaje de error", e], "=")

    finally:
        imprime([tiempo, datetime.now().strftime('%Y-%m-%d %H:%M:%S')], "* FIN TIEMPOS *")





# -----------------------------------------------
# Endpoints genéricos
# -----------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
@router.post("/apk_crea_tablas", response_model=InfoTransaccion,
             summary="🔄 ......................................",
             description="""..........................................................\n
                                - ✅ **Requiere autenticación**
                                - ✅ **Recibe un `id_App` y un `user`** para identificar al peticionario
                                - ✅ **Retorna `status` y `message` indicando error**
                         """,
             response_description="""📌 En caso de éxito retorna una clase InfoTransaccion y en resultados una lista json con cada BBDD/entidad/tabla tratada, tipo:\n
                                    {
                                        
                                    }
                                  """
            )
async def apk_crea_tablas(request: Request, body_params: ParamRequest = Body(...)):
    return await procesar_request(request, body_params, skd_crea_tablas, "apk_crea_tablas")



#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
@router.post("/apk_carga_tablas", response_model=InfoTransaccion,
             summary="🔄 ......................................",
             description="""..........................................................\n
                                - ✅ **Requiere autenticación**
                                - ✅ **Recibe un `id_App` y un `user`** para identificar al peticionario
                                - ✅ **Retorna `status` y `message` indicando error**
                         """,
             response_description="""📌 En caso de éxito retorna una clase InfoTransaccion y en resultados una lista json con cada BBDD/entidad/tabla tratada, tipo:\n
                                    {
                                        
                                    }
                                  """
            )
async def apk_carga_tablas(request: Request, body_params: ParamRequest = Body(...)):
    return await procesar_request(request, body_params, skd_carga_tablas, "apk_carga_tablas")



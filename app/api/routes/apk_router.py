from fastapi import APIRouter, HTTPException, Body, Request, Depends, File, UploadFile, Form
from datetime import datetime

from app.external_services.equinsa.servicios_equinsa import EquinsaService
from app.external_services.equinsa import crea_tablas, carga_tablas

from app.external_services.equinsa.servicios_equinsa import EquinsaService

# Importaciones propias del proyecto
# from app.external_services.equinsa import (
#     EquinsaService, crea_tablas
# )

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
# Endpoints optimizados
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
   
    return await procesar_request(request, body_params, crea_tablas, "apk_crea_tablas")



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
   
    return await procesar_request(request, body_params, carga_tablas, "apk_carga_tablas")



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
    print("Tiempos!!!-----------------------------------------", tiempo)
    try:
        # --------------------------------------------------------------------------------
        # Validaciones y construcción Básica
        # --------------------------------------------------------------------------------
        param = InfoTransaccion.from_request(body_params)

        control_usuario(param, request)

        # --------------------------------------------------------------------------------
        # Servicio
        # --------------------------------------------------------------------------------
        equinsa = EquinsaService(carpark_id="1237")

        # Ejecutar una consulta SQL
        sql_query = param.parametros[0] # "SELECT * FROM ope"
        resultado = equinsa.execute_sql_command(sql_query)
        # param.parametros.append(resultado["rows"])

        # Imprimir la respuesta
        imprime([type(resultado), resultado], '*   Mi primera select', 2)

        param.debug = f"Retornando un lista: {type(resultado["rows"])}"
        param.resultados = resultado["rows"] or []
        return param

    except Exception as e:
        # manejar_excepciones(e, param, "apk_consultas")
        imprime(["Mensaje de error", e], "=")

    finally:
        imprime([tiempo, datetime.now().strftime('%Y-%m-%d %H:%M:%S')], "* FIN TIEMPOS *")




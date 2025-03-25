from fastapi import APIRouter, HTTPException, Body, Request, Depends, File, UploadFile, Form
from datetime import datetime

from app.config.servicios_equinsa import EquinsaService
from app.services.externos.sistemas_control.equinsa import eqn_carga_tablas, eqn_crea_tablas

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
        equinsa = EquinsaService(carpark_id="1237")

        # Ejecutar una consulta SQL
        sql_query = param.parametros[0] # "SELECT * FROM ope"
        resultado = equinsa.execute_sql_command(sql_query)
        # param.parametros.append(resultado["rows"])

        # Imprimir la respuesta
        # imprime([type(resultado), resultado], '*   Mi primera select', 2)

        param.debug = f"Retornando un lista: {type(resultado["rows"])}"
        param.resultados = resultado["rows"] or []
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
    return await procesar_request(request, body_params, eqn_carga_tablas, "apk_carga_tablas")


#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
@router.post("/apk_cargar_tablas", response_model=InfoTransaccion,
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
async def apk_cargar_tablas(request: Request, body_params: ParamRequest = Body(...)):
    return await procesar_request(request, body_params, eqn_carga_tablas, "apk_cargar_tablas")




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
    return await procesar_request(request, body_params, eqn_crea_tablas, "apk_crea_tablas")




#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
class EqnsReservaCreaRequest(ParamRequest):
    product_type: int       #* Tipo de producto. Utilice el valor 1 para reservas monouso (cuando el vehículo abandona el parking la reserva finaliza independientemente del tiempo que reste hasta el final del intervalo seleccionado); el valor 2 es para reservas multiuso (el vehículo puede entrar y salir del parking sin restricciones dentro del intervalo de tiempo reservado).
    product_group_code: int #  Código del grupo de producto. Con esta variable puedes indicar el grupo de productos de la reserva. No puede ir en la misma peticion que la variable 'product_type', si esto ocurre, obtenedria el grupo de productos de la variable 'product_type'.
    rate_id: int            #  Identificador de la lista de precios a asignar.
    rate_description: int   #  Descipción de la lista de precios a asignar.
    permulresmismat: bool   #  ¿Permitir multiples reservas con la misma matricula?
    activation: str         #* Fecha/hora de inicio de la reserva.
    expiry: str             #* Fecha/hora de finalización de la reserva.
    license_plate: str      #* Número de matrícula del vehículo
    automatic_use_by_license_plate: bool #  Uso automático por matrícula. La barrera se abrirá automáticamente si cámara identifica la mátrícula como perteneciente a una reserva activa.
    holder_name: str               #  Nombre del usuario que realizó la reserva.
    reservation_generate_name: str #  Nombre de la digital que genera la reserva
    remarks: str             #  Texto asociado a la reserva. Lo genera la web que realiza la petición.
    reference_id: str        #  Identificador asociado a la reserva. Lo genera la web que realiza la petición.
    amount_paid: str         #* Importe pagado
    card_pan: str            #* Últimos 4 digitos de la tarjeta que realizo el pago
    card_transaction_no: str #* Identificador de la transacción
    card_operation_no: str   #* Número de operación

@router.post("/eqns_reserva_crea", response_model=InfoTransaccion,
             summary="🔄 Crea una reserva nueva (Nueva reserva con pago externo) - /reservations/externally_paid",
             description="""Un cliente hace una reserva\n
                                - ✅ **Requiere autenticación**
                                - ✅ **Recibe un `id_App` y un `user`** para identificar al peticionario
                                - ✅ **Retorna `status` y `message` indicando error**
                         """,
             response_description="""📌 En caso de éxito retorna una clase InfoTransaccion y en resultados una lista json con cada BBDD/entidad/tabla tratada, tipo:\n
                                    {
                                        
                                    }
                                  """
            )
async def eqns_reserva_crea(request: Request, body_params: ParamRequest = Body(...)):
    return await procesar_request(request, body_params, eqns_reserva_crea, "eqns_reserva_crea")



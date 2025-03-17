from cryptography.fernet import Fernet

from app.utils.mis_excepciones import MiException
from app.utils.InfoTransaccion import InfoTransaccion
from app.utils.utilidades import graba_log, imprime
from app.config.settings import settings
from app.services.db.ejec_proc import call_proc_bbdd


def proceso(param: InfoTransaccion) -> InfoTransaccion: 
    """
    Graba un registro en la tabla mail_access_token con el token encriptado.

    :param: Instancia de InfoTransaccion para gestionar parametros, logs y errores.
    :param.parametros[0]  --> tokenable: Tipo de recurso asociable al token.
    :param.parametros[1]  -->  name: Nombre descriptivo del token.
    :param.parametros[2]  -->  token: El token a encriptar.
    :param.parametros[3]  -->  abilities: Lista de habilidades del token.

    :return: Mensaje de éxito o error en param.ret_txt y ret_code

    Notas:
    - La clave de encriptación debe almacenarse de manera segura (por ejemplo, como variable de entorno).
    - Utiliza `os.environ` para cargar la clave desde el entorno y evitar exponerla en el código fuente.
    """
    funcion = "grabar_email.proceso"


    try:
        # id_servidor= param.parametros[0]
        # id_participante= param.parametros[1]
        # para= param.parametros[2]
        # para_nombre= param.parametros[3]
        # de= param.parametros[4]
        # de_nombre= param.parametros[5]
        # cc= param.parametros[6]
        # bcc= param.parametros[7]
        # prioridad= param.parametros[8]
        # reply_to= param.parametros[9]
        # clave_externa= param.parametros[10]
        # asunto= param.parametros[11]
        # cuerpo= param.parametros[12]
        # lenguaje= param.parametros[13]
        # parametros= param.parametros[14]
        # fecha_envio= param.parametros[15]
        # identificador_externo= param.parametros[16]

        # añadimos a parametros un cero, ya que es el del registro creado en caso de OK que retornamos en PARAM
        param.parametros.append(0) 
    
        param = call_proc_bbdd(param=param, procedimiento="w_mail_graba_mail")

        # Verificar si el procedimiento devolvió un error
        # if param.ret_code < 0:
        #     param.registrar_error(ret_code = param.ret_code, ret_txt=param.ret_txt, debug="llamada a procedimiento: w_mail_graba_mail")
        #     # raise MiException(param=param)
        #     graba_log(param, f"Excepción en {funcion}", None)

        return param

    except Exception as e:
        param.error_sistema(e=e, debug=f"Error no controlado en {funcion}")
        raise


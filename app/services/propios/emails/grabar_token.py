from cryptography.fernet import Fernet

from app.utils.mis_excepciones import MiException
from app.utils.InfoTransaccion import InfoTransaccion
from app.utils.utilidades import graba_log, imprime
from app.config.settings import settings
from app.services.db.ejec_proc import call_proc_bbdd


"""
GENERAR UNA CLAVE 64B para FERNET
from cryptography.fernet import Fernet

# Generar una nueva clave
new_key = Fernet.generate_key()
print(new_key.decode())  # Muestra la clave para configurarla como variable de entorno

"""


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
    funcion = "grabar_token.proceso"


    try:
        # tokenable = param.parametros[0] 
        # nombre = param.parametros[1] 
        token = param.parametros[2] 
        # abilities = param.parametros[3] 
        # ID = param.parametros[4] 

        # Obtener la clave de encriptación desde una variable de entorno
        encryption_key = settings.ENCRYPTION_KEY
        if not encryption_key:
            param.registrar_error(ret_txt= "La clave de encriptación no está configurada en las variables de entorno.", debug=f"{funcion}.encryption_key")
            raise MiException(param = param)

        fernet = Fernet(encryption_key)

        # Encriptar el token
        param.debug = token
        encrypted_token = fernet.encrypt(token.encode())
        param.parametros[2] = encrypted_token  # lo cambiamos por el token ya encriptado

        param.parametros.append(0) # añadimos a parametros un cero, ya que es el del registro creado en caso de OK que retornamos en PARAM

        param = call_proc_bbdd(param=param, procedimiento="w_mail_graba_access_token")

        # Verificar si el procedimiento devolvió un error
        if param.ret_code < 0:
            param.registrar_error(ret_code = param.ret_code, ret_txt=param.ret_txt, debug="llamada a procedimiento: w_mail_graba_access_token")
            raise MiException(param=param)
        
        return param

    except MiException as e:
        param.error_sistema(e=e, debug=f"Excepción en {funcion}")
        raise

    except Exception as e:
        param.error_sistema(e=e, debug=f"Error no controlado en {funcion}")
        raise


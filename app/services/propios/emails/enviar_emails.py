import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.utils.utilidades import graba_log

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Cc, Bcc, Content

from app.config.db_mallorquina import get_db_connection_mysql, close_connection_mysql
from app.services.auxiliares.sendgrid_service import enviar_email

from app.utils.utilidades import graba_log, imprime
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings
from app.utils.mis_excepciones import MiException


MAX_OFFSET: int = 400
SALTO: int = 0


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion):
    param.debug="proceso.Inicio"
    servidor: int = param.parametros[0]
    enviados = 0
    robinson = 0
    errores = 0
    offset = 0
    id_email = 0


    param.debug = "get_db_connection_mysql"
    try:
        conn_mysql = get_db_connection_mysql()
        cursor_mysql = conn_mysql.cursor(dictionary=True)

        param.debug = "datos conexión"
        datos_conexion = obtener_datos_conexion(param, conn_mysql, servidor)
        if not datos_conexion:
            raise MiException(param, f"No tenemos datos de conexión del servidor {servidor}", -1)

        while True:
            """ Procesa el envío de todos los emails pendientes """
            param.debug = "recger emails"
            emails = obtener_emails_pendientes(param, conn_mysql, servidor, offset)

            if not emails or len(emails) == 0 or offset > MAX_OFFSET:
                break

            offset += SALTO
            for email in emails:
                id_email = email["id"]
                param.debug = f'Enviar ({id_email}) para: {email["para"]} - CC: {email["cc"]} - BCC: {email["bcc"]}'
                resultado = enviar_email(param, conn_mysql, email, datos_conexion, servidor)  #  email["destinatario"], email["asunto"], email["cuerpo"]

                imprime(resultado, "*Resultado")

                if resultado[0] == 0:
                    param.debug = "Marcar Ok"
                    marcar_email(param, cursor_mysql, id_email, resultado[1], 'Ok')
                    enviados += 1
                elif resultado[0] == 1:
                    param.debug = "Marcar Robinson"
                    marcar_email(param, cursor_mysql, id_email, resultado[1], 'Robinson')
                    robinson += 1
                else:
                    param.debug = "Marcar Ko"
                    marcar_email(param, cursor_mysql, id_email, resultado[1], 'Ko')
                    errores += 1

                conn_mysql.commit()

        mensajes = [f"Se han enviado {enviados} emails."]
        if robinson != 0:
            mensajes.append(f"{robinson} no se han enviado por lista Robinson")
        if errores != 0:
            mensajes.append(f"{errores} han tenido algún tipo de error")

        return mensajes


    except Exception as e:
        param.error_sistema(e=e, txt_adic=f"emai: {id_email}", debug="proceso.Exception")
        raise 

    finally:
        close_connection_mysql(conn_mysql, cursor_mysql)


#----------------------------------------------------------------------------------------
# 'P'endiente de enviar;  
# 'E'rror de envío;  
# 'R'eintentar;  
# 'O'K;
# 'L'ista Robinson
#----------------------------------------------------------------------------------------
def marcar_email(param: InfoTransaccion, cursor_mysql, email_id, texto, estado):
    try:
        # 'P'endiente de enviar;  'E'rror de envío;  'R'eintentar;  'O'K; 'L'ista Robinson
        if estado == 'Ok':
            enviado = 'O'   
        elif estado == 'Ko':
            enviado = 'E'
        elif estado == 'Robinson':
            enviado = 'L'   # esto es dejarlo como está o intentar volver a enviar

        query = """UPDATE mail_envios 
                      SET estado = %s, 
                          error=%s, 
                          fecha_enviado=now()
                    WHERE id = %s"""
        cursor_mysql.execute(query, (enviado, texto, email_id,))

        

    except Exception as e:
        param.error_sistema(e=e, debug="marcar_email.Exception")
        raise 


#----------------------------------------------------------------------------------------
#      Envía un email utilizando SendGrid y los datos del servidor de correo
#----------------------------------------------------------------------------------------
def robinson(param: InfoTransaccion, conn_mysql, lista_emails, servidor):

    try:
        # imprime([lista_emails, type(lista_emails)], "*Primera")
        if isinstance(lista_emails, list):
            if not lista_emails:
                return []
        else:
            lista_emails = [lista_emails]

        cursor_mysql = conn_mysql.cursor(dictionary=True)

        # Si la lista es pequeña, usar WHERE IN
        if len(lista_emails) <= 500 and len(lista_emails) > 1:
            placeholders = ', '.join(['%s'] * len(lista_emails))
            # query = f"SELECT email FROM mail_robinson WHERE email IN ({placeholders})"
            query = "SELECT email FROM mail_robinson WHERE email IN (%s) and id_app = %s"
            cursor_mysql.execute(query, (lista_emails, servidor,))
            emails_en_robinson = {row[0] for row in cursor_mysql.fetchall()}  # Convertimos a set para búsqueda rápida
        else:
            emails_en_robinson = set()
            for email in lista_emails:
                cursor_mysql.execute("SELECT email FROM mail_robinson WHERE email = %s and id_app = %s", (email,servidor))
                resultado = cursor_mysql.fetchone()
                if resultado:
                    emails_en_robinson.add(resultado["email"])

        # Filtrar la lista original
        param.debug = "Filtrado 1"
        emails_filtrados = [email for email in lista_emails if email not in emails_en_robinson]
        if len(emails_filtrados) !=  len(lista_emails):
            raise MiException(param=param, detail="hay robinson en este correo", status_code=0) # no es un error como tal, pero no se puede enviar el email

        if settings.DEV_PROD == "DEV":
            param.debug = "Filtrado 2"
            lista_validos = ['lvicente@hangarxxi.com', 'lvicenteperea@gmail.com']
            emails_filtrados = [email for email in emails_filtrados if email in lista_validos]


        return emails_filtrados or []

    except MiException as e:
        raise e
                
    except Exception as e:
        import traceback
        print("🔥 Error capturado:", str(e))
        traceback.print_exc() 
        raise MiException(param=param, detail="Se ha producido un error al calcular la lsita robinson", status_code=0) #Es un error , pero solo lo vamos a marcar como que no se puede enviar el email
                

    finally:
        cursor_mysql.close()



#----------------------------------------------------------------------------------------
#      Envía un email utilizando SendGrid y los datos del servidor de correo
#----------------------------------------------------------------------------------------
def enviar_email(param: InfoTransaccion, conn_mysql, email, datos_conexion, servidor):
    
    try:
        # Inicializar el cliente SendGrid con la API Key desde datos_conexion
        param.debug = "password"
        sg = sendgrid.SendGridAPIClient(api_key=datos_conexion["password"])

        # Configurar el remitente
        param.debug = "de_nombre"
        from_email = Email(datos_conexion["de"], datos_conexion["de_nombre"])

        # Configurar destinatarios principales (TO)
        param.debug = "para"
        lista = robinson(param, conn_mysql, email["para"], servidor)
        param.debug = "para2"
        to_emails = [To(dest) for dest in lista] if isinstance(lista, list) else [To(lista)]

        # Configurar CC (Con Copia)
        param.debug = "cc"
        lista = robinson(param, conn_mysql, email.get("cc", []), servidor)
        cc_emails = [Cc(dest) for dest in lista] if len(lista)>0 else []

        # Configurar BCC (Con Copia Oculta)
        param.debug = "bcc"
        lista = robinson(param, conn_mysql, email.get("bcc", []), servidor)
        bcc_emails = [Cc(dest) for dest in lista] if len(lista)>0 else []

        # Configurar contenido del email
        param.debug = "asunto"
        subject = email["asunto"]
        content = Content("text/html", email["cuerpo"])

        # Construcción del email
        param.debug = "Mail"
        mail = Mail(from_email, to_emails, subject, content)

        # Agregar CC y BCC si existen
        param.debug = "cc y bcc"
        if cc_emails:
            mail.personalizations[0].add_cc(cc_emails)
        if bcc_emails:
            mail.personalizations[0].add_bcc(bcc_emails)

        # Configurar el "Reply-To"
        param.debug = "reply_to"
        if "reply_to" in datos_conexion:
            mail.reply_to = Email(datos_conexion["reply_to"])

        # Enviar el email
        param.debug = "cargar response"
        response = sg.client.mail.send.post(request_body=mail.get())

        param.debug = "status_code"
        if response.status_code in [200, 202]:
            return [0, "Ok"]
        else:
            return [-1, f"Error: {response}"]


    except MiException as e:
        return [1, "Hay un elemento en este email que es lista robinson"]  # no es un error, simplemente hay que marcarlo como robinson

    except Exception as e:
        return [-1, str(e)]


    

#----------------------------------------------------------------------------------------
#         Obtiene los emails pendientes de la base de datos
#----------------------------------------------------------------------------------------
def obtener_emails_pendientes(param: InfoTransaccion, conn_mysql, servidor, offset):
    try:
        cursor_mysql = conn_mysql.cursor(dictionary=True)

        query = "SELECT * FROM mail_envios WHERE id_servidor = %s AND estado in ('P', 'R') order by prioridad limit 100 OFFSET %s"

        cursor_mysql.execute(query, (servidor, offset,))
        emails = cursor_mysql.fetchall()

        return emails

    except Exception as e:
        param.error_sistema(e=e, debug="obtener_emails_pendientes.Exception")
        raise 

    finally:
        cursor_mysql.close()


#----------------------------------------------------------------------------------------
#         Obtiene los datos de CONEXION con el proveedor de servcio de EMAIL
#----------------------------------------------------------------------------------------
def obtener_datos_conexion(param: InfoTransaccion, conn_mysql, servidor):
    try:
        cursor_mysql = conn_mysql.cursor(dictionary=True)
        
        query = "SELECT * FROM mail_servidores WHERE id = %s order by orden_servidor"

        cursor_mysql.execute(query, (servidor,))

        datos = cursor_mysql.fetchone()

        return datos

    except Exception as e:
        param.error_sistema(e=e, debug="obtener_datos_conexion.Exception")
        raise 

    finally:
        cursor_mysql.close()        
        
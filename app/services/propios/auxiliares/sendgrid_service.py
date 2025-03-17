# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# from config.config import SENDGRID_API_KEY

def enviar_email(lista_emails, asunto, contenido):
    '''
    message = Mail(
        from_email="notificaciones@tuempresa.com",
        to_emails=lista_emails.split(','),
        subject=asunto,
        html_content=contenido
    )
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)
    '''    
    print("enviar_email.01", lista_emails)
    print("enviar_email.asunto", asunto)
    print("enviar_email.contenido", contenido)
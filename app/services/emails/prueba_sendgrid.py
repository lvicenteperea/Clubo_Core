import sendgrid
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = "tu_api_key"  # O usa os.getenv("SENDGRID_API_KEY")

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

email = Mail(
    from_email="it@pastelerialamallorquina.es",
    to_emails="destinatario@ejemplo.com",
    subject="Prueba de SendGrid",
    html_content="<strong>¡Hola! Este es un email de prueba con SendGrid.</strong>"
)

response = sg.send(email)
print(response.status_code)
print(response.body)
print(response.headers)
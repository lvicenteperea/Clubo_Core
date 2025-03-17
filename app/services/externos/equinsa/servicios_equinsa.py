import os
import base64
import requests
from app.config.settings import settings

class EquinsaService:
    def __init__(self, carpark_id: str):
        """Inicializa el servicio con el ID del parking y credenciales desde variables de entorno."""
        self.carpark_id = carpark_id
        self.api_user =  settings.API_EQUINSA_USER    #  os.getenv("API_EQUINSA_USER", "clubo")
        self.api_password = settings.API_EQUINSA_PWR  #  os.getenv("API_EQUINSA_PWR", "AG8t3B2q")
        self.base_url = "https://tunel.equinsaparking.com/EPCloud/api/parking"

        # Generar el token de autenticación en base64
        self.auth_header = self._generate_auth_header()


    def _generate_auth_header(self):
        """Genera el header de autenticación en Base64."""
        credentials = f"{self.api_user}:{self.api_password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded_credentials}", "Accept": "application/json"}

    def execute_sql_command(self, sql_command: str):
        """Ejecuta un comando SQL en la API de Equinsa."""
        url = f"{self.base_url}/{self.carpark_id}/system/sql"
        payload = {"command": sql_command}

        try:
            response = requests.post(url, json=payload, headers=self.auth_header)
            response.raise_for_status()  # Lanza un error si la respuesta no es 2xx
            return response.json()

        except requests.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None

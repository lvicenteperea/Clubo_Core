# con la nueva versión de pedantic, la variables deben ser anotadas:
from pydantic_settings import BaseSettings
# from typing import ClassVar

class Settings(BaseSettings):
    PROJECT_NAME: str = "Clubo Core API"

    RUTA_LOCAL: str = "C:/GitHub/Clubo_Core/"
    RUTA_BASE: str = "app/ficheros/"
    RUTA_IMAGEN: str = "app/ficheros/imagen/"
    RUTA_DATOS: str = "app/ficheros/datos/"


    # ----------------------------------------------------------------------------------------
    # CONEXIONES
    # ----------------------------------------------------------------------------------------
    # Coenxión SSH ---------------------------------------------------------------------------
    SSH_HOST: str = 'xxx.xxx.xxx'
    SSH_PORT: int = 15122
    SSH_USER: str = 'xxxxx'
    # SSH_key_path: str = '/ruta/a/tu/clave/privada.pem' # Cambia por ssh_password si usas contraseña
    SSH_PWD: str = 'xxxx'
    # LOCAL MYSQL ----------------------------------------------------------------------------
    SSH_CONEX: bool = False
    MYSQL_DB_HOST_MLL: str = "127.0.0.1"
    MYSQL_DB_PORT_MLL: int = 3306
    MYSQL_DB_USER_MLL: str = 'root'  # Añadimos anotación de tipo
    MYSQL_DB_PWD_MLL: str = 'Admin'  # Añadimos anotación de tipo
    MYSQL_DB_HOST_MLL: str = 'localhost'  # Añadimos anotación de tipo
    MYSQL_DB_DATABASE_MLL: str = 'clubo-data'  # Añadimos anotación de tipo
    MYSQL_DB_CHARSET: str = "utf8mb4"

   
    # ----------------------------------------------------------------------------------------
    
    MONGODB_URL: str = ""

    ENCRYPTION_KEY: str = "ZOoYUEQNjONU2fwUv-afUuUA--Z4RZlvRL4evOY_ZJk="
    AUTH_ENABLED: bool = False  # Cambiar a False para desactivar la autenticación

    LOG_LEVEL: str = "info"

    # para el API de Equinsa
    API_EQUINSA_USER: str ="clubo"
    API_EQUINSA_PWR: str = "AG8t3B2q"



    class Config:
        env_file = ".env"

settings = Settings()
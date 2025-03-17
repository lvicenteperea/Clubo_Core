from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from app.config.settings import settings

from app.utils.utilidades import graba_log, imprime

"""
Lo ideal es que se guarde en el sistema:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_dev_secret")

Pero podemos generala nosotros, sobre todo para desarrollo    
    import secrets

    SECRET_KEY = secrets.token_hex(32)  # Genera una clave de 64 caracteres (32 bytes)
    print(SECRET_KEY)
"""
SECRET_KEY = "71400d095eacde5d73d9621e4c6383672279ad437c08666ac0e5244c3928fd89"
ALGORITHM = "HS256"


class AuthMiddleware(BaseHTTPMiddleware):
    # Esquema de autenticación
    security = HTTPBearer()



 # -----------------------------------------------------------------------------------------------
    # Control de Acceso opr IP
    # -----------------------------------------------------------------------------------------------
    '''
        Si la aplicación está detrás de un proxy o balanceador de carga, como Nginx, la IP del cliente 
        puede no ser precisa. En este caso, utiliza el header X-Forwarded-For:

            @app.middleware("http")
            async def restrict_ip_middleware(request: Request, call_next):
                forwarded_for = request.headers.get("x-forwarded-for")
                client_ip = forwarded_for.split(",")[0] if forwarded_for else request.client.host

                allowed_ips = ["127.0.0.1", "192.168.1.100"]
                if client_ip not in allowed_ips:
                    return JSONResponse({"detail": "Acceso denegado"}, status_code=403)

                return await call_next(request)
    '''
    @staticmethod
    def validate_ip(client_ip: str) -> bool:
        allowed_ips = ["127.0.0.1", "192.168.1.100"]  # Lista de IPs permitidas
        return client_ip in allowed_ips


    #----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------    
    async def dispatch(self, request: Request, call_next):
        # print(f"Headers recibidos: {request.headers}")
        # print("")
        # print("")

        # Validar IP
        client_ip = request.client.host
        if not self.validate_ip(client_ip):
            print(f"Acceso denegado para la IP: {client_ip}")
            return JSONResponse({"detail": "Acceso denegado"}, status_code=403)        
        
        # Excluir ciertas rutas de autenticación
        if request.url.path in ["/login", "/open-endpoint", "/docs", "/redoc", "/auth/create_token", "/openapi.json", "/auth/login"]:
            return await call_next(request)

        # Obtener token del encabezado Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            imprime([auth_header, request.headers.get("Authorization"), request.url.path], "*")
            return JSONResponse({"detail": "Autenticación requerida1"}, status_code=401)

        token = auth_header.split(" ")[1]

        # Agrega un registro para identificar las solicitudes que fallan debido a la ausencia del encabezado:
        if not auth_header or not auth_header.startswith("Bearer "):
            print(f"Fallo de autenticación en {request.url.path}: encabezado Authorization ausente o incorrecto")
            return JSONResponse({"detail": "Autenticación requerida2"}, status_code=401)

        request.state.user = self.get_current_user(token)

        return await call_next(request)


    #----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------    
    @staticmethod
    def get_current_user(token): #credentials):

        try:
            if settings.AUTH_ENABLED:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #credentials.credentials
                # print(payload.get("user"), payload)
                return payload.get("user")
            else:
                return "usuario_dev"
            
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Token inválido o expirado2")
        
    #----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------    
    @staticmethod
    def create_token(data: dict) -> str:
        """
        Genera un token JWT con los datos proporcionados.
        
        Args:
            data (dict): Datos a incluir en el token (ejemplo: user, id_App, exp).
            
        Returns:
            str: Token JWT firmado.
        """
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
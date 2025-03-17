# Lo siguiente:
#     utilizar los middleware


# uvicorn app.main:app --reload
# python -m uvicorn app.main:app --reload
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI, HTTPException #, Request  #, Depends
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse

# from app.api.routes import router as api_router
from app.api.routes.mll_router import router as mallorquina_router
from app.api.routes.auth_router import router as auth_router
from app.api.routes.email_router import router as email_router

from app.api.routes.apk_router import router as aparcamientos_router



from app.middleware.auth import AuthMiddleware
import json 


from app.exceptions import http_exception_handler, json_decode_error_handler, generic_exception_handler, mi_exception_handler, type_error_handler
from app.config.settings import settings
from app.utils.mis_excepciones import MiException
from app.middleware.log_tiempos_respuesta import log_tiempos_respuesta

# -----------------------------------------------------------------------------------------------
# FASTAPI
# -----------------------------------------------------------------------------------------------
app = FastAPI(  title=settings.PROJECT_NAME,
                description="Documentación de mi API con FastAPI",
                version="1.0",
                docs_url="/docs",  # URL de Swagger UI
                redoc_url="/redoc"  # URL de ReDoc
             )

# -----------------------------------------------------------------------------------------------
# LOGS
# -----------------------------------------------------------------------------------------------
# Importar y registrar el middleware
app.middleware("http")(log_tiempos_respuesta)

# -----------------------------------------------------------------------------------------------
# RUTAS
# -----------------------------------------------------------------------------------------------
# app.include_router(api_router)
app.include_router(mallorquina_router, prefix="/mallorquina", tags=["Mallorquina"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(email_router, prefix="/email", tags=["Email"])

app.include_router(aparcamientos_router, prefix="/aparcamientos", tags=["Clubo"])

# -----------------------------------------------------------------------------------------------
# AUTENTICACIÓN
# -----------------------------------------------------------------------------------------------
app.add_middleware(AuthMiddleware)


# -----------------------------------------------------------------------------------------------
# EXCEPTION HANDLERS
# -----------------------------------------------------------------------------------------------
app.add_exception_handler(MiException, mi_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(json.JSONDecodeError, json_decode_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(TypeError, type_error_handler)



# -----------------------------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------------------------
# Configurar CORS para permitir peticiones desde React (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo a ["http://localhost:3000"] si solo es React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



'''
# -----------------------------------------------------------------------------------------------
# MIDDLEWARES
# -----------------------------------------------------------------------------------------------
app.add_middleware(LoggingMiddleware)
app.add_middleware(ExceptionMiddleware)
app.add_middleware(AuthMiddleware)



# -----------------------------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------------------------
# Configuración de CORS
origins = [
    "http://localhost",            # Tu frontend local
    "http://localhost:3000",       # Otro puerto local, por ejemplo, para React
    "https://yourdomain.com",      # Tu dominio principal
    "https://*.yourdomain.com"     # Todos los subdominios
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Permitir estos dominios
    allow_credentials=True,          # Permitir cookies/credenciales
    allow_methods=["*"],             # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],             # Permitir todas las cabeceras
)
'''

'''
Este bloque de código se usa para iniciar la aplicación FastAPI utilizando uvicorn 
como servidor cuando ejecutas directamente el script Python. 
Es un método estándar para lanzar aplicaciones web con FastAPI y asegurar que el servidor 
web esté escuchando en el puerto y dirección IP correctos, con la configuración de logging adecuada.
'''
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=settings.LOG_LEVEL)



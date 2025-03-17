from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class MailEnvio(BaseModel):
    id: Optional[int]           = Field(None, description="Identificador único del envío")
    id_app: int                 = Field(..., description="Identificador de la aplicación")
    id_servidor: int            = Field(..., description="Identificador del servidor")
    id_participante: int        = Field(..., description="Identificador del participante")
    estado: str                 = Field("P", description="Estado del correo ('P'endiente, 'E'rror, 'R'eintento, 'O'K, 'L'ista Robinson)")
    para: str                   = Field(..., max_length=255, description="Correo del destinatario")
    para_nombre: Optional[str]  = Field(None, max_length=255, description="Nombre del destinatario")
    de_: str                    = Field(..., max_length=255, alias="de", description="Correo del remitente")
    de_nombre: Optional[str]    = Field(None, max_length=255, description="Nombre del remitente")
    cc: Optional[str]           = Field(None, description="Correos en copia")
    bcc: Optional[str]          = Field(None, description="Correos en copia oculta")
    prioridad: int              = Field(3, description="Prioridad del correo (valor por defecto 3)")
    reply_to: Optional[str]     = Field(None, max_length=255, description="Dirección de respuesta")
    clave_externa: Optional[str] = Field(None, max_length=255, description="Clave externa asociada al envío")
    asunto: str                 = Field(..., max_length=255, description="Asunto del correo")
    cuerpo: str                 = Field(..., description="Cuerpo del correo, puede ser HTML")
    lenguaje: str               = Field(..., max_length=255, description="Lenguaje del correo")
    parametros: Optional[str]   = Field(None, description="Parámetros adicionales en formato JSON")
    fecha_envio: datetime       = Field(..., description="Fecha en la que se planificó el envío")
    fecha_enviado: Optional[datetime] = Field(None, description="Fecha en la que se realizó el envío")
    error: Optional[str]            = Field(None, description="Texto con errores acumulativos de envío")
    identificador_externo: Optional[str] = Field(None, max_length=255, description="ID del envío en el proveedor de servicios")
    created_at: datetime            = Field(..., description="Fecha de creación del registro")
    updated_at: Optional[datetime]  = Field(None, description="Fecha de última actualización")
    modified_by: Optional[str]      = Field(None, max_length=45, description="Usuario que realizó la última modificación")

    class Config:
        orm_mode = True  # Permite compatibilidad con modelos de SQLAlchemy
    '''
    Ventajas de esta implementación:
    Compatibilidad con SQLAlchemy:

    La opción orm_mode = True permite que los modelos trabajen directamente con bases de datos.
    Validaciones automáticas:

    Se establecen valores predeterminados y validaciones como longitud máxima de cadenas.
    '''


class MailEnvioAdjunto(BaseModel):
    id: Optional[int] = Field(None, description="Identificador único del adjunto")
    id_envio: int = Field(..., description="Identificador del envío de correo")
    id_adjunto: int = Field(..., description="Identificador del adjunto")
    created_at: datetime = Field(..., description="Fecha de creación del registro")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")
    modified_by: Optional[str] = Field(None, max_length=45, description="Usuario que realizó la última modificación")

    class Config:
        orm_mode = True


    '''
    Modelo combinado para incluir adjuntos en un envío:
        class MailEnvioWithAdjuntos(MailEnvio):
            adjuntos: Optional[List[MailEnvioAdjunto]] = Field(None, description="Lista de adjuntos relacionados con el envío")

    Ejemplo de uso en una ruta FastAPI:
        from fastapi import FastAPI
        app = FastAPI()

        @app.get("/enviar-correo/{id_envio}", response_model=MailEnvioWithAdjuntos)
        async def get_enviar-correo(id_envio: int):
            mail_envio = get_mail_envio_with_adjuntos(id_envio)
            return mail_envio

        @app.post("/enviar-correo/", response_model=MailEnvio)
        async def enviar_correo(mail: MailEnvio):
            # Simulación de lógica de guardado
            return mail
    
    '''
from typing import Optional
from pydantic import BaseModel
from typing import List, Dict

class ContenidoRequest(BaseModel):
    tipo_campo: str
    nombre: str
    valor1: Optional[str] = None
    valor2: Optional[str] = None


class ListaContenidosResponse(BaseModel):
    codigo_error: int
    mensaje: Optional[str] = None
    lista: List[Dict[str, str]]
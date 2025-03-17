from typing import Optional, Dict, Any
from pydantic import BaseModel

class ValidaUrlResponse(BaseModel):
    codigo_error: int
    mensaje: str
    # datos: Optional[Dict[str, Any]] = None
    # datos: Optional[list] = None

    id_Frontal: Optional[int] = None
    id_Catalogo: Optional[int] = None
    

    def asigna_salida(self, param: list):
        self.id_Frontal = param[2]
        self.id_Catalogo = param[3]

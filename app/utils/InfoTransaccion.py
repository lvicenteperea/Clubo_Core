from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Any
import json
import traceback


from app.utils.utilidades import graba_log, imprime

class ParamRequest(BaseModel):
    id_App: int = 1           # aplicación a la que conectarse  
    user: str = "usuario_dev" # usuario de autenticación en el servidor
    ret_code: int = 0         # debería llegar siempre a cero
    ret_txt: str = "OK"       # Debería llegar siempre a Ok o vacio



class InfoTransaccion(BaseModel):
    id_App: int = 0
    user: str = 'Sistema_' # Usuario de sistema que se conecta: Fronta, BackOfficce, un servicio específico, webs de terceros...
    ret_code: int = 0
    ret_txt: str = "Ok"
    debug: str = "" # solo por si se necesita saber por donde ha pasado la ejecución

    parametros: Optional[List[Any]] = None  # Parámetros específicos que ha recibido el servicio, función,....
    resultados: List[Any] = []  # Lista vacía predeterminada para resultados, siempre será una lista, con un texto, varios, con un listado.....
    

    @classmethod
    def from_request(cls, request: ParamRequest) -> "InfoTransaccion":
        # Extraer los valores de los atributos base
        base_data = request.dict(exclude_unset=True)
        
        # Extraer los parámetros adicionales (los que no están en ParamRequest)
        base_fields = set(ParamRequest.__annotations__.keys())
        extra_params = {k: v for k, v in base_data.items() if k not in base_fields}
        
        # Construcción del campo debug con todos los valores
        debug_info = " - ".join([f"{key}: {value}" for key, value in base_data.items()])
        
        return cls(
            **{k: v for k, v in base_data.items() if k in base_fields},  # Solo los campos base
            parametros=list(extra_params.values()),  # Lista con valores extra
            debug=debug_info
        )


    def set_parametros(self, datos):
        self.parametros = datos

    def set_resultados(self, datos):
        self.resultados = datos

    def registrar_error(self, ret_txt: str, ret_code: int = -1, debug: str = ""):
        self.ret_code = ret_code
        self.ret_txt = ret_txt
        if debug:
            self.debug = debug

    # --------------------------------------------------------------------------------------------------------
    # Va a ser una EXCEPTION controlada o no, pero siempre es una salida abrupta del programa
    # --------------------------------------------------------------------------------------------------------
    def error_sistema(self, e: Exception = None, txt_adic: str = '.', debug: str = ""):
        loc = ""
        param = self.copy()

        if self.ret_code != -99:
            if self.ret_code is None or self.ret_code >= 0:
                self.ret_code = -99
            param.ret_txt = f"{self.ret_txt}{txt_adic}"
            param.debug = self.debug if not debug else f"{self.debug} + {debug}"

            
            if isinstance(e, BaseException): # Comprueba si es una excepción, Debería serlo siempre
                tb = traceback.extract_tb(e.__traceback__)
                archivo, linea, funcion, texto_err = tb[-1]
                loc = f'{texto_err.replace("-", "_")} - {archivo.replace("-", "_")} - {linea} - {funcion}'

            imprime([f"param: {self}",
                    f"Excepción: {str(e) if e else 'No es una excepción'}",
                    f"Parametros: {txt_adic}, {debug}",
                    f"Traza: {loc}",
                    ],"* --- LOG error_sistema --- ",2)

            graba_log(param, f"error_sistema: {loc}", e)


    #----------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------
    def limpiar_error(self):
        self.ret_code = None
        self.ret_txt = None
        self.debug = None

    #----------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------
    def to_list(self):
        return [self.id_App, self.user, self.ret_code, self.ret_txt]

    #----------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------
    def to_list_proc_bbdd(self):

        lista = [self.id_App, self.user, self.ret_code, self.ret_txt]

        for item in self.parametros:
            # lista.append(item)
            if isinstance(item, list):
                lista.append(','.join(map(str, item)))  # Convertir listas a cadenas separadas por comas
            elif isinstance(item, dict):
                lista.append(json.dumps(item))  # Convertir diccionarios a formato JSON
            else:
                lista.append(item)  # Mantener el valor original si es un tipo compatible

        return lista

    #----------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------
    def to_infotrans_proc_bbdd(self, list: list):
        return InfoTransaccion( id_App      = list[0], 
                                user        = list[1], 
                                ret_code    = list[2], 
                                ret_txt     = list[3] if list[3] else "", 
                                parametros  = list[4:]
                           )

    def to_dict(self):
        return {"id_app": self.id_App, "Usuario": self.user, "ret_code": self.ret_code, "ret_txt": self.ret_txt, "debug": self.debug}
        #return {"id_app": self.id_App, "Usuario": self.user, "ret_code": self.ret_code, "ret_txt": self.ret_txt, "debug": self.debug, "parametros": self.parametros, "resultados": self.resultados}
    
    def __str__(self):
        return f"App: {self.id_App}, Usuario: {self.user}, Error: {self.ret_code} - {self.ret_txt}, debug: {self.debug}, parametros: {self.parametros}"
    






    def sistem_error(self, txt_adic: str = '.', debug: str = ""):
        if self.ret_code is None or self.ret_code >= 0:
            self.ret_code = -99
            self.ret_txt = f"Error general. contacte con su administrador ({datetime.now().strftime('%Y%m%d%H%M%S')}){txt_adic}"
        
        self.debug = self.debug if not debug else debug

    
from fastapi import HTTPException
import json

from app.utils.InfoTransaccion import InfoTransaccion
from app.utils.utilidades import graba_log, imprime
from app.config.db_mallorquina import get_db_connection_mysql, close_connection_mysql

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def call_proc_bbdd(param: InfoTransaccion, procedimiento:str, conn_mysql = None, commit: bool = True) -> InfoTransaccion:
    """
        Este método ejecuta un procedimiento almacenado en la base de datos, toma los parámetros 
        necesarios, y devuelve una instancia de `InfoTransaccion` que contiene 
            - Variables de salida
            - Recorset retornado por el procedimiento en formato JSON

        Parámetros:
        -----------
        procedimiento : str
            El nombre del procedimiento almacenado que se va a ejecutar.
        param : lista
            Lista de paramostros que debe coincidir con los del procedimiento de BBDD
            Si hay un elemneto de la lista de tipo `InfoTransaccion` los expande en la lista.

        Retorna:
        --------
        InfoTransaccion
            Una instancia de `InfoTransaccion` que contiene:
            - `id_App`: Identificador de la aplicación.
            - `user`: El usuario que hace la solicitud.
            - `ret_code`: Código de retorno del procedimiento (0 indica éxito, valores negativos indican error).
            - `ret_txt`: Texto de retorno con un mensaje o descripción.
            - `resultados`: Si la ejecución es exitosa, contiene los resultados del procedimiento en formato JSON.

        Excepciones:
        ------------
        HTTPException
            Se lanza si ocurre un error durante la ejecución del procedimiento o durante el procesamiento de los resultados.

        Ejemplo de Uso:
        ---------------
        ```
        info_trans = call_proc_bbdd_records("mi_procedimiento", mi_param)
        if info_trans.ret_code == 0:
            print("Procedimiento ejecutado con éxito")
            print("Resultados:", info_trans.resultados)
        else:
            print("Error:", info_trans.ret_txt)
        ```

        Notas:
        ------
        - El método expande los parámetros proporcionados usando `expande_lista` para adaptarlos a la llamada al 
        procedimiento almacenado.
        - Después de la ejecución, se procesan los resultados y se convierten a JSON antes de devolverlos.
        - El método maneja la conexión a la base de datos y garantiza su cierre incluso si ocurre una excepción.
    """
    
    if not conn_mysql:
        llega_con_connexion = True
        conn_mysql =  get_db_connection_mysql()
    else:
        llega_con_connexion = False
    
    try:
        # Crear una nueva lista para almacenar los elementos expandidos, ya que param debe trar un tipo InfoTransaccion
        #param_expanded = expande_lista(param)
        param_proc = param.to_list_proc_bbdd()

        cursor = conn_mysql.cursor()
        response = cursor.callproc(procedimiento, param_proc)

        # Se crea yba variable infoTrans pque es la respuesta con con los datos de infoTrans que es una lista que retorna el procedimiento en variables
        infoTrans = InfoTransaccion().to_infotrans_proc_bbdd(response)
        if infoTrans.ret_code < 0:
            return infoTrans
    
        # para convertirlo a JSON el posible record set retornado
        rows = []
        for result in cursor.stored_results():
            columns = [col[0] for col in result.description]  # Obtener nombres de las columnas
            rows = [
                    {col: (val if val is not None else "") for col, val in zip(columns, row)}
                    for row in result.fetchall()
                   ]  # Convertir cada fila en un diccionario, reemplazando None con ""
        
        # Convertir la lista de diccionarios a JSON
        json_rows = json.dumps(rows)
        infoTrans.set_resultados(json.loads(json_rows))

        if commit and not llega_con_connexion: # si llega con conexión no haceamos commit porque no sabemos que ha pasado antes.....
            conn_mysql.commit()

        return infoTrans

    except Exception as e:
        param.error_sistema(e=e, debug="proceso.Exception")
        raise 

    finally:
        if llega_con_connexion:
            cursor.close()
        else:
            close_connection_mysql(conn_mysql, cursor)




#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def ejec_select(query:str, param, conn_mysql = None):
 
    if not conn_mysql:
        llega_con_connexion = True
        conn_mysql =  get_db_connection_mysql()
    else:
        llega_con_connexion = False
    
    try:
        cursor = conn_mysql.cursor(dictionary=True)  # Para obtener los resultados como diccionarios
        cursor.execute(query)
        resultado = cursor.fetchall()  # Obtener los resultados como lista de diccionarios

        return resultado
  
    except Exception as e:
        raise HTTPException(status_code=400, detail={"ret_code": -3,
                                                     "ret_txt": str(e),
                                                     "excepcion": e
                                                    }
                           )
    finally:
        if llega_con_connexion:
            cursor.close()
        else:
            close_connection_mysql(conn_mysql, cursor)


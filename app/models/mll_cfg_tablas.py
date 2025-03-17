import re

from app.utils.utilidades import graba_log, imprime
from app.utils.InfoTransaccion import InfoTransaccion

#----------------------------------------------------------------------------------------     
#----------------------------------------------------------------------------------------
def obtener_campos_tabla(conn, id_entidad, id_tabla):

    # cursor = conn.cursor(dictionary=True)
    # cursor.execute("SELECT * FROM mll_cfg_campos WHERE ID_Tabla = %s", (id_tabla,))
    # campos = cursor.fetchall()
    # cursor.close()

    query = """SELECT a.*, b.ult_valor FROM mll_cfg_campos a
                inner join mll_cfg_tablas_entidades b on a.id_tabla = b.id_tabla and id_entidad = %s
                WHERE a.ID_Tabla = %s
                ORDER BY a.orden"""
                # ORDER BY CASE 
				#			WHEN a.PK = 0 THEN 99 
				#			ELSE a.PK 
				#		   END"""
    # imprime([id_bbdd, id_tabla, query], '$')
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (id_entidad, id_tabla))
    campos = cursor.fetchall()
    # imprime([campos], '%')
    cursor.close()

    return campos

#----------------------------------------------------------------------------------------
"""
def crear_tabla_destino(param: InfoTransaccion, conn_mysql, nombre_tabla, campos):
    try:
        param.debug = "Creando tabla destino"
        cursor = conn_mysql.cursor()

        # columnas = ", ".join([f"{campo['Nombre_Destino']} {campo['Tipo']}" for campo in campos])
        " ""
        re.search(r'{(.+?)}', campo['Nombre']):
            - Busca contenido dentro de las llaves {} en campo['Nombre'].
            - Si encuentra algo, devuelve un objeto de búsqueda (Match).
        
        re.search(...).group(1):
            - Extrae el contenido dentro de las llaves {} (el texto sin las llaves).
        
        {'default ' + contenido if ... else ''}:
            - Si el contenido dentro de las llaves existe, añade default seguido del contenido extraído.
            - Si no hay llaves, no añade nada adicional.
        
        .strip():
            - Elimina espacios adicionales al final de la cadena generada.
        "" "

        columnas = ", ".join([
            f"{campo['Nombre_Destino']} {campo['Tipo']} {'default ' + re.search(r'{(.+?)}', campo['Nombre']).group(1) if re.search(r'{(.+?)}', campo['Nombre']) else ''}".strip()
            for campo in campos
        ])
        imprime([type(campos), campos], '*campos',2)
        imprime([type(columnas), columnas], '*Columnas',2)
        z=1/0
        if not columnas:
            raise f"No hay columnas definidas para la tabla {nombre_tabla}"

        columnas += ", Origen_BBDD VARCHAR(100)"
        query = f"" "CREATE TABLE IF NOT EXISTS {nombre_tabla} 
                        (ID INT NOT NULL AUTO_INCREMENT,
                        {columnas},
                        created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
                        modified_by varchar(45) DEFAULT NULL,
                        PRIMARY KEY (`ID`))
                    ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4"" "

        param.debug = query
        cursor.execute(query)
        conn_mysql.commit()

    except Exception as e:
        param.error_sistema(e=e)
        graba_log(param, "recorre_tiendas.Exception", e)
        raise e
    
    finally:
        cursor.close()
"""  
#----------------------------------------------------------------------------------------
def crear_tabla_destino(param: InfoTransaccion, conn_mysql, nombre_tabla, campos):
    try:
        param.debug = "Creando tabla destino"
        cursor = conn_mysql.cursor()
        columnas = None
        # imprime([nombre_tabla, campos], '*Creando tabla',2)

        from datetime import datetime

        # Lista de datos simulada
        resultado = []

        for item in campos:
            nombre = item["Nombre"].strip("{}")
            nombre_destino = item["Nombre_Destino"]
            tipo = item["Tipo"]

            if nombre == "stIdEnt":
                resultado.append(f"{nombre_destino} {tipo} DEFAULT 'SIN DEFINIR'")
            elif "{" in nombre and "}" in nombre:
                valor_entre_llaves = nombre.strip("{}")
                resultado.append(f"{nombre_destino} {tipo} DEFAULT {valor_entre_llaves}")
            else:
                resultado.append(f"{nombre_destino} {tipo}")

        if len(resultado) == 0:
            raise f"No hay columnas definidas para la tabla {nombre_tabla}"

        # Unir los elementos con coma, excepto el último
        columnas = ", ".join(resultado)
        columnas += ", Origen_BBDD VARCHAR(100)"

        query = f"""CREATE TABLE IF NOT EXISTS {nombre_tabla} 
                        (ID INT NOT NULL AUTO_INCREMENT,
                        {columnas},
                        created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
                        modified_by varchar(45) DEFAULT NULL,
                        PRIMARY KEY (`ID`))
                    ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4"""

        param.debug = query
        cursor.execute(query)
        conn_mysql.commit()

    except Exception as e:
        param.error_sistema(e=e, debug="recorre_tiendas.Exception")
        raise e
    
    finally:
        cursor.close()
    
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def drop_tabla(conn_mysql, tabla):
    cursor_mysql = conn_mysql.cursor()
    cursor_mysql.execute(f"DROP TABLE IF EXISTS {tabla}")
    cursor_mysql.close()

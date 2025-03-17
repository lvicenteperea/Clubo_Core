from datetime import datetime
import re

from app.utils.utilidades import graba_log, imprime

from app.config.db_mallorquina import get_db_connection_sqlserver, close_connection_sqlserver

from app.utils.InfoTransaccion import InfoTransaccion
from app.utils.mis_excepciones import MiException

# PAGINACION: int = 500   ... esto no está hecho para tablas en las que haya que paginar....

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion, conn_mysql, entidad, tabla, bbdd_config, campos, tabla_config) -> list:  # retorna el [valor_max, insertados, Actualizados]
    param.debug="proceso_general"
    cursor_mysql = None # para que no de error en el finally
    valor_max = None
    insertados = 0
    actualizados = 0
    txt_conexion = None
    # salto = 0  ... esto no está hecho para tablas en las que haya que paginar....
    try:
        proximo_valor = tabla["ult_valor"]
        nombre_tabla_destino = tabla_config['Tabla_Destino'] 
        nombre_tabla_origen  = tabla_config['Tabla_Origen'] 
        # imprime([entidad], "* --- entidad ---", 2)
        # imprime([bbdd_config], "* --- bbdd_config ---", 2)
        # imprime([nombre_tabla], "* --- nombre_tabla ---", 2)
        # imprime([tabla_config], "* --- tabla_config ---", 2)
        # imprime([tabla], "* --- tabla ---", 2)
        # imprime([campos], "* --- campos ---", 2)
        # z=1/0

        while True:
            registros,lista_pk,lista_max_valor,txt_conexion = Obtener_datos_origen(param, entidad, bbdd_config, nombre_tabla_origen, campos, tabla_config["campos_PK"], proximo_valor) # , salto)
            if len(registros) == 0:
                break

            # salto += PAGINACION  ... esto no está hecho para tablas en las que haya que paginar....

            param.debug = "A por los campos"
            # Identificar el campo PK basado en mll_cfg_campos
            pk_campos = [campo for campo in campos if campo.get("PK", 0) >= 1]
            if not pk_campos:
                param.registrar_error(ret_txt=f"No se encontró ningún campo PK en {nombre_tabla_origen}.", debug=f"Campos: {campos}")
                raise MiException(param = param)

            # Usamos el primer campo PK encontrado
            pk_campo = pk_campos[0]["Nombre_Destino"]
            campos_update = [campo for campo in campos if campo["Nombre_Destino"] != pk_campo]

            param.debug = "comando_insert"
            # Generar consultas INSERT y UPDATE de forma dinamica
            insert_query = comando_insert(campos, nombre_tabla_destino)
            param.debug = "comando_update"
            update_query = comando_update(campos_update, pk_campo, nombre_tabla_destino)

            param.debug = "Bucle registros"
            # Preparar los cursores para MySQL
            cursor_mysql = conn_mysql.cursor()
            for registro in registros:
                # Obtener el valor del campo PK desde el registro
                pk_index = [campo["Nombre"] for campo in campos].index(pk_campos[0]["Nombre"])
                pk_value = registro[pk_index]

                proximo_valor = ", ".join(str(registro[i]) for i in lista_max_valor)
                param.debug = f"Proximo valor: {proximo_valor}"

                if "U" in tabla_config["insert_update"]:
                    if nombre_tabla_destino == "___tpv_salones_restaurante":
                        select = f"""SELECT COUNT(*) 
                                    FROM {nombre_tabla_destino} 
                                    WHERE {pk_campo} = %s
                                      AND  stIdEnt = {entidad["stIdEnt"]}
                                      AND Origen_BBDD = {entidad["id_bbdd"]}"""
                    else:
                        select = f"""SELECT COUNT(*) 
                                    FROM {nombre_tabla_destino} 
                                    WHERE {pk_campo} = %s
                                        AND Origen_BBDD = {entidad["id_bbdd"]}"""

                    # Comprobar si el registro ya existe en la tabla destino
                    cursor_mysql.execute(select, (pk_value,))
                    existe = cursor_mysql.fetchone()[0] > 0  # Si existe, devuelve True
                else:
                    # Solo actualizo último valor recogido cuando es una tabla de insert, porque se entiende que inserta desde el registro que se ha quedado
                    existe = False # no se comprueba que exista, ya que no se hacaen updates
                    valor_max = proximo_valor

                if existe:
                    # Realizar un UPDATE
                    campos_update_filtrado = [campo for campo in campos_update if not (campo['Nombre'].startswith('{') and campo['Nombre'].endswith('}'))]
                    valores_update = [registro[[campo["Nombre"] for campo in campos].index(campo["Nombre"])]
                                                for campo in campos_update_filtrado] + [pk_value, entidad["id_bbdd"]]
                    # imprime(["update:......", pk_value, update_query, valores_update], "=......UPDATE......")
                    cursor_mysql.execute(update_query, valores_update)
                    actualizados += cursor_mysql.rowcount
                else:
                    # Realizar un INSERT
                    registro_destino = list(registro) + [entidad["id_bbdd"]]  # Campos + Origen
                    # if insert_query.count(", stIdEnt)") == 1:
                    #     registro_destino += [entidad['stIdEnt']] # Campos + stIdEnt
                    # if insert_query.count(", id_entidad)") == 1:
                    #     registro_destino += [entidad['ID']] # Campos + id_entidad

                    # if any(campo["Nombre"] == "{stIdEnt}" for campo in campos):
                    if  existe_en_campos(campos, "{stIdEnt}"):
                        registro_destino += [entidad['stIdEnt']] # Campos + stIdEnt

                    # if any(campo["Nombre"] == "{id_entidad}" for campo in campos):
                    if  existe_en_campos(campos, "{id_entidad}"):
                        registro_destino += [entidad['ID']] # Campos + id_entidad


                    # imprime([insert_query, registro_destino, entidad], "=......INSERT......", 2)
                    cursor_mysql.execute(insert_query, registro_destino)
                    insertados += cursor_mysql.rowcount

                param.debug = "Execute fec_ult_act"
                cursor_mysql.execute("""UPDATE mll_cfg_tablas_entidades
                                        SET Fecha_Ultima_Actualizacion = %s, 
                                            ult_valor = COALESCE(%s, ult_valor)
                                        WHERE ID = %s""",
                                    (datetime.now(), valor_max, tabla["ID"])   # valor_max solo tiene sentido en Insert, en update igual habría que hacerlo manual o pensarlo...
                                    )
            conn_mysql.commit()

        return [valor_max, insertados, actualizados, txt_conexion]

    except Exception as e:
        param.error_sistema(e=e, debug="proceso_general.Exception")
        raise 



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
# Función para convertir datetime en string
# def convertir_fechas(tupla):
#     return tuple(
#         elemento.strftime("%Y-%m-%d %H:%M:%S") if isinstance(elemento, datetime) else elemento
#         for elemento in tupla
#     )


def Obtener_datos_origen(param: InfoTransaccion, entidad, bbdd_config, nombre_tabla, campos, campos_PK, ult_valor) -> list: 
    param.debug="Inicio"
    conn_sqlserver = None # para que no de error en el finally
    cursor_sqlserver = None # para que no de error en el finally
    registros = []
    lista_pk = []

    try:
        param.debug = "conn origen"
        try:
            # conextamos con esta bbdd origen
            conn_sqlserver = get_db_connection_sqlserver(bbdd_config)
        except Exception as e:
            return [ [], [], [], "No se ha podido conectar con la BBDD origen"]

        # Leer datos desde SQL Server
        param.debug = "crear cursor"
        cursor_sqlserver = conn_sqlserver.cursor()
        if not ult_valor:
            param.debug = f"No hay ult_valor para la tabla {nombre_tabla}, con los campos {campos_PK}"
            raise ValueError("No se ha proporcionado un valor para ult_valor.")

        # Contruimos la SELECT que va a recoger los datos de ORIGEN
        param.debug = "Construir Select"
        select_query, lista_pk, lista_max_valor = construir_consulta(param, entidad, campos, nombre_tabla, campos_PK, ult_valor) # ya no se recibe como parametro, salto)

        # Ejecución del cursor
        # imprime([select_query], "*")
        param.debug = "Ejecutar select"
        cursor_sqlserver.execute(select_query)

        registros = cursor_sqlserver.fetchall()
        # datos = cursor_sqlserver.fetchall()
        # registros = [convertir_fechas(tupla) for tupla in datos]
        # imprime(registros, "* --- REGISTROS ---",2)

        return [registros, lista_pk, lista_max_valor, None]

    except Exception as e:
        param.error_sistema(e=e, debug="Obtener_datos_origen.Exception")
        raise 

    finally:
        param.debug = f"cierra conexión sqlserver: {param.debug}"
        close_connection_sqlserver(conn_sqlserver, cursor_sqlserver)

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def construir_consulta(param: InfoTransaccion, entidad, campos, nombre_tabla, campos_PK, ult_valor) -> list: 
    try:
        # Construcción de la lista de campos para la SELECT
        campos_select = [campo['Nombre'] for campo in campos if not campo['Nombre'].startswith('{')]
        
        lista_pk_valores = [item.strip('" ') for item in ult_valor.split(", ")]

        lista_pk_campos, lista_pk_formato, lista_pk_para_order = separar_campos_pk(campos_PK)

        condiciones_where = generar_where(param, lista_pk_campos, lista_pk_valores, lista_pk_formato, lista_pk_para_order)

        lista_max_valor = []

        # Construcción del WHERE
        condiciones_order = []
        lista_pk = list()
        for campo in campos:
            campo_pk = campo.get('PK')
            if campo_pk != 0: # Sabemos su es un indice
                lista_max_valor.append(campo_pk - 1) # Este lo vamos a utiliar para luego guardar el max_valor cargado

                if campo_pk-1 in lista_pk_para_order: # solo estos se deben utilizar para el order y el where
                    lista_pk.append(campo_pk ) #carga_lista_pk(lista_pk, formato, ccampo_pk-1)         
                    condiciones_order.append(f"{campo['Nombre']}")

        # Generar la consulta SQL
        query = f"SELECT {', '.join(campos_select)} FROM {nombre_tabla} {condiciones_where}"
        if condiciones_order:
            query += f" ORDER BY {' , '.join(condiciones_order)}"

            # ... esto no está hecho para tablas en las que haya que paginar....
            # query = f"""{query} 
            #         OFFSET {salto} ROWS            -- Salta 0 filas
            #         FETCH NEXT {PAGINACION} ROWS ONLY; -- Toma las siguientes 100"""
        

        # imprime([query, lista_pk, lista_max_valor], "*  construir_consulta", 2)

        return [query, lista_pk, lista_max_valor]

    except Exception as e:
        param.error_sistema(e=e, debug="Obtener_datos_origen.Exception")
        raise 


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def separar_campos_pk(cadena):
    """
        cfg_tables.campos_pk debe tener un formato de 3 partes encerradas entre parentesis:
        - La primera parte son los nombres de los campos entre comillas (")
        - La segunda es como transformar cada uno de esos campos para hacer el where, 
            teniendo en cuenta que {V1} es el nombre del campo (de la zona anterior) y {V2} va a ser el valor del campo
        - La tercera será los campos que realmente van a formar parte del where
            
        ejemplo de la cadena mostrada en tres lineas para identificarlo mejor:
            ("stIdEnt"; "Fecha"; "[Serie Puesto Facturacion]"; "[Factura Num]"; "[Id Relacion]") 
            ("{v1} >= '{v2}'"; "{v1} >= CONVERT(DATETIME, '{v2}', 121) "; "{v1} >= '{v2}'"; "{v1} >= {v2}"; "{v1} >= {v2}") 
            (1) o (0; 1) ...  --> tener en cuenta que los elementos empiezan en el 0 y el separador es el punto y coma

        
    """
    # Separar las dos partes
    partes = cadena.split(") (")
    if len(partes) != 3:
        raise ValueError("La cadena debe contener dos partes separadas por ') ('.")
    
    # Limpiar paréntesis iniciales y finales
    parte1 = partes[0].strip("()")
    parte2 = partes[1].strip("()")
    parte3 = partes[2].strip("()")
    
    # Convertir cada parte en listas separando por comas
    lista_campos = [item.strip().strip('"') for item in parte1.split(";")]
    lista_formatos = [item.strip().strip('"') for item in parte2.split(";")]
    lista_orden_str = [item.strip().strip('"') for item in parte3.split(";")] # deben ser números pero crea la lista de str
    # imprime(lista_orden_str, "*Orden")
    lista_orden = []
    for cadena in lista_orden_str:
        try:
            lista_orden.append(int(cadena))
        except ValueError:
            print(f"No se puede convertir '{cadena}' a número.")

    if len(lista_campos) != len(lista_formatos):
        raise ValueError(f"Las dos listas han de tener el mismo número de elementos y tienen {len(lista_campos)} y {len(lista_formatos)} elementos")
    
    return lista_campos, lista_formatos, lista_orden


#----------------------------------------------------------------------------------------
# generamos el where de origen con los datos de las tres lista de elementos que tengo:
#   - Campos de la tabla original que son PK
#   - Ultimos valores utilizados, debemos empezar a trabajar desde ahí
#   - Posible conversión de datos, a fechas,....
#----------------------------------------------------------------------------------------
def generar_where(param: InfoTransaccion, lista_pk_campos, lista_pk_valores, lista_pk_formato, lista_pk_para_where):
    try:    
        # Verificar que todas las listas tengan la misma longitud

        # imprime([lista_pk_campos, lista_pk_valores, lista_pk_formato], "*  Lista PK2", 2)

        if not (len(lista_pk_campos) == len(lista_pk_valores) == len(lista_pk_formato)):
            param.debug = f"Campos({len(lista_pk_campos)}): {lista_pk_campos}  --  Valores ({len(lista_pk_valores)}): {lista_pk_valores}  --  Formato ({len(lista_pk_formato)}): {lista_pk_formato}"
            raise ValueError("Las listas deben tener la misma longitud.")
        
        # Construir la cláusula WHERE
        where_clause = []
        for i, (col, val, template) in enumerate(zip(lista_pk_campos, lista_pk_valores, lista_pk_formato)):
            if i in lista_pk_para_where:
                if not template:  # Si lista_pk_formato no tiene valor, usar el formato básico
                    if isinstance(val, str):  # Si el valor es una cadena, mantener las comillas
                        where_clause.append(f"{col} >= \"{val}\"")
                    else:  # Si no es una cadena, usar el valor tal cual
                        where_clause.append(f"{col} >= {val}")
                else:  # Si lista_pk_formato tiene valor, usar el formato proporcionado
                    formatted_value = template.replace("{v1}", str(col)).replace("{v2}", str(val))
                    where_clause.append(formatted_value)
        
        # Unir las condiciones con AND
        return f"WHERE {' AND '.join(where_clause)}"

    except Exception as e:
        param.error_sistema(e=e, debug="generar_where.Exception")
        raise 
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def carga_lista_pk(lista, valor, posicion, relleno=None):
    # Rellenar la lista si la posición está fuera de rango
    while len(lista) <= posicion:
        lista.append(relleno)
    
    # Insertar el valor en la posición indicada
    lista[posicion] = valor

    return lista


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def comando_insert(campos, nombre_tabla_destino):
    columnas_mysql = [campo["Nombre_Destino"] for campo in campos if not campo["Nombre"].startswith("{")]
    columnas_mysql.append("Origen_BBDD")
    # Si existe un campo con 'Nombre' igual a '{stIdEnt}', agregamos 'stIdEnt' a la lista
    # if any(campo["Nombre"] == "{stIdEnt}" for campo in campos):
    if  existe_en_campos(campos, "{stIdEnt}"):
        columnas_mysql.append("stIdEnt")

    # if any(campo["Nombre"] == "{id_entidad}" for campo in campos):
    if  existe_en_campos(campos, "{id_entidad}"):
        columnas_mysql.append("id_entidad")

    return f"""
            INSERT INTO {nombre_tabla_destino} ({', '.join(columnas_mysql)})
            VALUES ({', '.join(['%s'] * len(columnas_mysql))})
            """

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def comando_update(campos_update, pk_campo, nombre_tabla_destino):
    """
    re.match(r"^{.+}$", campo["Nombre"]):
        - Verifica si campo["Nombre"] comienza con { y termina con }.
    
    re.search(r"{(.+?)}", campo["Nombre"]).group(1):
        - Extrae el contenido entre las llaves {} en campo["Nombre"].
    
    Condición en la comprensión de lista:
        - Si campo["Nombre"] cumple con la condición de llaves, genera Nombre_Destino = contenido_dentro_de_las_llaves.
        - Si no cumple, genera Nombre_Destino = %s.
    
    ', '.join([...]):
        - Combina todas las asignaciones generadas en una sola cadena separada por comas.
    """
    update_query = f"""UPDATE {nombre_tabla_destino}
                        SET {', '.join([
                            f'{campo["Nombre_Destino"]} = {re.search(r"{(.+?)}", campo["Nombre"]).group(1)}' if re.match(r"^{.+}$", campo["Nombre"]) 
                            else f'{campo["Nombre_Destino"]} = %s' 
                            for campo in campos_update
                        ])}
                        WHERE {pk_campo} = %s AND Origen_BBDD = %s
                   """
    return update_query



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def existe_en_campos(campos, valor):
    return any(campo["Nombre"] == valor for campo in campos)
      


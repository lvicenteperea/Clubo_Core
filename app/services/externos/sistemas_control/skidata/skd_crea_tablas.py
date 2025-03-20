import re

from app.config.servicios_equinsa import EquinsaService

from app.utils.utilidades import graba_log, imprime
from app.config.db_clubo import get_db_connection_mysql, close_connection_mysql
from app.config.db_clubo import get_db_connection_sqlserver, close_connection_sqlserver
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings

def proceso(param: InfoTransaccion) -> list:
    resultado = []
    param.debug = "proceso"
    # punto_venta = param.parametros[1]

    bbdd_config = {"host": "192.168.17.99", "port": "1433", "user": "onlineuser", "database": "PARK_DB", "password": "Not4LocalUsers!"} # obtener_conexion_bbdd_origen(conn_mysql, ID_NUBE)
    param.debug = "conectamos con esta bbdd origen"
    conn_sqlserver = get_db_connection_sqlserver(bbdd_config)
    cursor_sqlserver = conn_sqlserver.cursor()

    query = """SELECT 
                    c.table_name,
                    c.COLUMN_NAME,
                    c.ORDINAL_POSITION,
                    c.DATA_TYPE,
                    c.CHARACTER_MAXIMUM_LENGTH,
                    c.NUMERIC_PRECISION,
                    c.NUMERIC_SCALE,
                    c.IS_NULLABLE,
                    k.CONSTRAINT_NAME AS PRIMARY_KEY
                FROM INFORMATION_SCHEMA.COLUMNS c
                LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE k 
                    ON c.TABLE_NAME = k.TABLE_NAME 
                    AND c.COLUMN_NAME = k.COLUMN_NAME
                    AND k.CONSTRAINT_NAME IN (
                        SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE = 'PRIMARY KEY'
                    )
                ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION"""
    
    param.debug = "Ejecutamos cursor"
    cursor_sqlserver.execute(query)
    # datos = cursor_sqlserver.fetchall()
    param.debug = "recuperamos"
    datos = cursor_sqlserver.fetchall()
    param.debug = "Cerramos conexión"
    close_connection_sqlserver(conn_sqlserver,  cursor_sqlserver)
    # resultado = [sublista[0] for sublista in datos]
    resultado = [list(tupla) for tupla in datos]

    columns_info = resultado

    # Mapeo de tipos de datos
    data_type_map = {
        "int": "INT",
        "bigint": "BIGINT",
        "smallint": "SMALLINT",
        "tinyint": "TINYINT",
        "bit": "TINYINT(1)",
        "decimal": "DECIMAL",
        "numeric": "DECIMAL",
        "float": "FLOAT",
        "real": "FLOAT",
        "datetime": "DATETIME",
        "smalldatetime": "DATETIME",
        "date": "DATE",
        "time": "TIME",
        "char": "CHAR",
        "varchar": "VARCHAR",
        "nvarchar": "VARCHAR",
        "text": "TEXT",
        "ntext": "TEXT"
    }

    # Procesar datos y generar los scripts
    tables = {}

    param.debug = "Por Aquí 01"
    for row in columns_info:
        # Ejemplo de ROW: ['ValidationProviders', 'MinRate',              12,   'float',                    None,                53,          None,        'NO', None]
        #                  table_name,          COLUMN_NAME,ORDINAL_POSITION, DATA_TYPE,CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE, IS_NULLABLE, CONSTRAINT_NAME AS PRIMARY_KEY
        table_name = row[0]
        column_name = row[1]
        data_type = row[3]
        char_length = str(row[4])
        if char_length:
            char_length = char_length.replace('-1','100')
        num_precision = row[5]
        num_scale = row[6]
        is_nullable = "NULL" if row[7] == "YES" else "NOT NULL"
        primary_key = row[8]

        # Convertir tipos de datos
        if data_type in ["varchar", "nvarchar", "char"]:
            column_type = f"{data_type_map[data_type]}({char_length})"
        elif data_type in ["decimal", "numeric"]:
            column_type = f"{data_type_map[data_type]}({num_precision},{num_scale})"
        else:
            column_type = data_type_map.get(data_type, "TEXT")

        # Agregar columnas a la tabla
        if table_name not in tables:
            tables[table_name] = []

        column_definition = f"`{column_name}` {column_type} {is_nullable}"
        tables[table_name].append((column_definition, primary_key))

    # Generar los scripts CREATE TABLE
    scripts = []
    for table, columns in tables.items():
        primary_keys = [col[0] for col in columns if col[1] is not None]
        column_definitions = ",\n    ".join([col[0] for col in columns])

        # Cadena original
        cadena = ', '.join(primary_keys)
        imprime([cadena], "*  CADENA")

        # Usar una expresión regular para extraer los nombres de las columnas
        lista_columnas = re.findall(r'`([^`]+)`', cadena)

        # Unir los nombres de las columnas con comas
        columnas = ', '.join(f'`{col}`' for col in lista_columnas)
        primary_key_def = f",\n    PRIMARY KEY ({columnas})" if primary_keys else ""

        script = f"CREATE TABLE `skd_{table}` (\n    {column_definitions}{primary_key_def}\n);"
        scripts.append(script)

    # Guardar los scripts en un archivo
    with open("tables_mysql_skidata.sql", "w", encoding="utf-8") as f:
        for script in scripts:
            f.write(script + "\n\n")

    print("✅ Scripts generados en 'tables_mysql_skidata.sql'")


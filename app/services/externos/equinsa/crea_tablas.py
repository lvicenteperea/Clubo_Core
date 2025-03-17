import pyodbc
import os
import shutil
from datetime import datetime

from app.external_services.equinsa.servicios_equinsa import EquinsaService

from app.utils.utilidades import graba_log, imprime
from app.config.db_mallorquina import get_db_connection_mysql, close_connection_mysql
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings

def proceso(param: InfoTransaccion) -> list:
    resultado = []
    param.debug = "proceso"
    # punto_venta = param.parametros[1]

    equinsa = EquinsaService(carpark_id="1237")
    sql_query = """SELECT 
                    c.TABLE_NAME,
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
    resultado = equinsa.execute_sql_command(sql_query)
    columns_info = resultado["rows"]

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


    for row in columns_info:
        table_name = row['table_name']
        column_name = row['column_name']
        data_type = row['data_type']
        char_length = row['character_maximum_length']
        num_precision = row['numeric_precision']
        num_scale = row['numeric_scale']
        is_nullable = "NULL" if row['is_nullable'] == "YES" else "NOT NULL"
        primary_key = row['primary_key']

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

        primary_key_def = f",\n    PRIMARY KEY ({', '.join(primary_keys)})" if primary_keys else ""

        script = f"CREATE TABLE `{table}` (\n    {column_definitions}{primary_key_def}\n);"
        scripts.append(script)

    # Guardar los scripts en un archivo
    with open("create_tables_mysql.sql", "w", encoding="utf-8") as f:
        for script in scripts:
            f.write(script + "\n\n")

    print("✅ Scripts generados en 'create_tables_mysql.sql'")


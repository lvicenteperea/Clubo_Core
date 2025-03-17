from datetime import datetime

from app.external_services.equinsa.servicios_equinsa import EquinsaService

from app.utils.utilidades import graba_log, imprime
from app.config.db_mallorquina import get_db_connection_mysql, close_connection_mysql
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings


# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion) -> list:
    resultado = []
    param.debug = "proceso"
    # punto_venta = param.parametros[1]
    equinsa = EquinsaService(carpark_id="1237")
    param.parametros.append(equinsa)


    try:
        # Conectar a la base de datos
        conn_mysql = get_db_connection_mysql()
        cursor_mysql = conn_mysql.cursor(dictionary=True)

        tablas = recupera_tablas(param, equinsa)

        for tabla in tablas:
            columnas = recupera_columnas(param, equinsa, tabla)

            """Genera un SELECT dinámico con las columnas dadas para obtener datos"""
            datos = obtener_datos_origen(param, equinsa, columnas, tabla)
            
            """Genera un SELECT dinámico con las columnas dadas"""
            insert_query = generar_insert(param, tabla, columnas)

            insert_datos(param, cursor_mysql, tabla, insert_query, datos)
            conn_mysql.commit()


        print("✅ Inserción realizada")

    except Exception as e:
        param.error_sistema(e=e, debug="proceso.Exception")
        raise 

    finally:
        param.debug = "cierra conn"
        close_connection_mysql(conn_mysql, cursor_mysql)
    
# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def recupera_tablas(param: InfoTransaccion, equinsa) -> list: 
    sql_query = """SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"""

    datos_equinsa = equinsa.execute_sql_command(sql_query)
    resultado = datos_equinsa["rows"]
    tablas = [item['table_name'] for item in resultado]

    return tablas

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def recupera_columnas(param: InfoTransaccion, equinsa, tabla: str) -> list: 
    sql_query = f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name = '{tabla}' ORDER BY ORDINAL_POSITION"

    datos_equinsa = equinsa.execute_sql_command(sql_query)
    resultado = datos_equinsa["rows"]
    columnas = [item['column_name'] for item in resultado]

    return columnas

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def obtener_datos_origen(param: InfoTransaccion, equinsa, columnas, tabla):
    columnas_str = ", ".join(columnas)
    sql_query = f"SELECT {columnas_str} FROM {tabla};"

    datos_equinsa = equinsa.execute_sql_command(sql_query)
    datos = datos_equinsa["rows"]

    return datos        

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def generar_insert(param: InfoTransaccion, tabla, columnas):
    """Genera una sentencia INSERT INTO con los valores extraídos"""
    columnas_str = ", ".join(columnas)
    placeholders = ", ".join(["%s"] * len(columnas))  # Placeholders para evitar inyección SQL
    insert_query = f"INSERT INTO {tabla} ({columnas_str}) VALUES ({placeholders})"

    return insert_query


# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def insert_datos(param: InfoTransaccion, cursor_mysql, tabla, insert_query, datos_dict):
    """Ejecuta el INSERT en la base de datos MySQL destino"""
    param.debug = f"insertando en tabla: {tabla}"

    datos_dict_ok = convertir_todo(datos_dict)

    # columnas = ['fechorfin', 'fechorini', 'nompc', 'nomapl', 'pidapl', 'ruteje', 'finfor', 'nomusu', 'verapl']
    columnas = list(datos_dict_ok[0].keys())
    datos = [tuple(row.get(col, None) for col in columnas) for row in datos_dict_ok]
     

    imprime([datos, len(datos), type(datos), insert_query], '*   INSERT', 2)

    cursor_mysql.executemany(insert_query, datos)

    print(f"{cursor_mysql.rowcount} registros insertados en {tabla}.")


# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def convertir_todo(datos_dict):
    for row in datos_dict:
        for key, value in row.items():
            if isinstance(value, str) and "/" in value:
                row[key] = convertir_fecha(value)
    return datos_dict



def convertir_fecha(fecha_str):
    if not fecha_str:
        return None  # O dejarlo como está si es null
    try:
        # Si viene con hora
        if " " in fecha_str:
            dt = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M:%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            # Si solo es fecha sin hora
            dt = datetime.strptime(fecha_str, "%d/%m/%Y")
            return dt.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error convirtiendo fecha {fecha_str}: {e}")
        return fecha_str  # Devuelve la original si falla

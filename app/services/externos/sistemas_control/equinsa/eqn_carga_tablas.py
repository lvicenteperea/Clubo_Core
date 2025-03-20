from datetime import datetime
import time

from app.config.servicios_equinsa import EquinsaService

from app.utils.utilidades import graba_log, imprime
from app.config.db_clubo import get_db_connection_mysql, close_connection_mysql
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings

"""
truncate table `clubo-data`._hissesbd;
truncate table `clubo-data`._ver;
truncate table `clubo-data`.c_tipapa;
truncate table `clubo-data`.c_ins;
truncate table `clubo-data`.apa;


SELECT * FROM `clubo-data`._hissesbd;
SELECT * FROM `clubo-data`._ver;
SELECT * FROM `clubo-data`.c_tipapa;
SELECT * FROM `clubo-data`.c_ins;
SELECT * FROM `clubo-data`.apa;
-- 'apa', 'c_tipsop', 'apeman', 'c_condetcob', 'c_contot', 'c_estpre', 'c_forpag', 'c_gruparcon', 'c_gruper', 'c_parcon', 'c_per', 'c_resautpro', 'c_subtipapa', 'c_tipinc', 'c_tipmanpro', 'c_tipopeaud', 'c_tipopecaj', 'c_tippro', 'camapa', 'capima', 'car', 'cli', 'grucli', 'cligrucli', 'ope', 'tur', 

SELECT * FROM `clubo-data`.c_subtipapa
"""
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

        # tablas = recupera_tablas(param, equinsa)
        # tablas = ['_hissesbd', '_ver', 'c_tipapa', 'c_ins', 'apa', 'c_tipsop', 'apeman', 'c_condetcob', 'c_contot', 'c_estpre', 'c_forpag', 'c_gruparcon', 'c_gruper', 'c_parcon', 'c_per', 'c_resautpro', 'c_subtipapa', 'c_tipinc', 'c_tipmanpro', 'c_tipopeaud', 'c_tipopecaj', 'c_tippro', 'camapa', 'capima', 'car', 'cli', 'grucli', 'cligrucli', 'ope', 'tur', 'cob', 'comeve', 'con', 'decperope', 'lispre', 'tar', 'rec', 'hor', 'profuecir', 'proencir', 'grupro', 'detcob', 'opecaj', 'detopecaj', 'plazon', 'zon', 'entsal', 'enu', 'envinc', 'equgruproins', 'res', 'fac', 'fes', 'frahor', 'fratar', 'inc', 'inssis', 'lisnegmat', 'lisnegpro', 'manpro', 'remtarcre', 'opetarcre', 'parcon', 'paslispre', 'perope', 'polacc', 'regaud', 'regcon', 'regpreusu', 'remrecdom', 'traren', 'renpro', 'tarpro', 'tottur', 'traerrsis', 'vehcli', 'veropepro']
        tablas = ['cob']
        
        for tabla in tablas:
            columnas = recupera_columnas(param, equinsa, tabla)

            """Genera un SELECT dinámico con las columnas dadas para obtener datos"""
            datos = obtener_datos_origen(param, equinsa, columnas, tabla)
            if datos:
                """Genera un SELECT dinámico con las columnas dadas"""
                insert_query = generar_insert(param, tabla, columnas)

                insert_datos(param, cursor_mysql, tabla, insert_query, datos)
                conn_mysql.commit()

            time.sleep(10)
    
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
    param.debug = "recupera_tablas"
    sql_query = """SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"""

    datos_equinsa = equinsa.execute_sql_command(sql_query)
    resultado = datos_equinsa["rows"]
    tablas = [item['table_name'] for item in resultado]

    return tablas

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def recupera_columnas(param: InfoTransaccion, equinsa, tabla: str) -> list: 
    param.debug = f"recupera_columnas {tabla}"
    sql_query = f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name = '{tabla}' ORDER BY ORDINAL_POSITION"

    datos_equinsa = equinsa.execute_sql_command(sql_query)
    resultado = datos_equinsa["rows"]
    columnas = [item['column_name'] for item in resultado]

    return columnas

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def obtener_datos_origen(param: InfoTransaccion, equinsa, columnas, tabla):
    param.debug = f"obtener_datos_origen {tabla}"
    columnas_str = ", ".join(columnas)
    sql_query = f"SELECT {columnas_str} FROM {tabla};"

    datos_equinsa = equinsa.execute_sql_command(sql_query)
    if datos_equinsa:
        datos = datos_equinsa["rows"]
    else:
        datos = []
    return datos        

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def generar_insert(param: InfoTransaccion, tabla, columnas):
    param.debug = f"generar_insert {tabla}"
    """Genera una sentencia INSERT INTO con los valores extraídos"""
    columnas_str = ", ".join(columnas)
    placeholders = ", ".join(["%s"] * len(columnas))  # Placeholders para evitar inyección SQL
    insert_query = f"INSERT INTO eqn_{tabla} ({columnas_str}) VALUES ({placeholders})"

    return insert_query


# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def insert_datos(param: InfoTransaccion, cursor_mysql, tabla, insert_query, datos_dict):
    """Ejecuta el INSERT en la base de datos MySQL destino"""
    param.debug = f"insertando en tabla: {tabla}"

    if datos_dict:
        datos_dict_ok = convertir_todo(datos_dict)
        columnas = list(datos_dict_ok[0].keys())
        datos = [tuple(row.get(col, None) for col in columnas) for row in datos_dict_ok]

        imprime([datos, len(datos), insert_query], f"= {tabla}", 2)
        instruccion = insert_query.replace(", sql,", ", `sql`,")
        instruccion = instruccion.replace(", mod,", ", `mod`,")

        cursor_mysql.executemany(instruccion, datos)

        print(f"{cursor_mysql.rowcount} registros insertados en {tabla}.")
    else:
        print(f"0 registros insertados en {tabla}.")


# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def convertir_todo(datos_dict):
    for row in datos_dict:
        for key, value in row.items():
            if isinstance(value, str) and "/" in value and (len(value)==10 or len(value)==19):
                row[key] = convertir_fecha(value)
            elif es_numero(value):
                row[key] = value.replace(',', '.') if isinstance(value, str) else value

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


def es_numero(valor):
    try:
        # Reemplazar coma por punto antes de validar
        valor = valor.replace(',', '.') if isinstance(valor, str) else valor
        float(valor)
        return True
    except (ValueError, TypeError):
        return False

from datetime import datetime
import time

from app.config.servicios_equinsa import EquinsaService

from app.utils.utilidades import graba_log, imprime
from app.config.db_clubo import get_db_connection_mysql, close_connection_mysql
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

        # tablas = recupera_tablas(param, equinsa)
        # tablas = ['_hissesbd', '_ver', 'c_tipapa', 'c_ins', 'apa', 'c_tipsop', 'apeman', 'c_condetcob', 'c_contot', 'c_estpre', 'c_forpag', 'c_gruparcon', 'c_gruper', 'c_parcon', 'c_per', 'c_resautpro', 'c_subtipapa', 'c_tipinc', 'c_tipmanpro', 'c_tipopeaud', 'c_tipopecaj', 'c_tippro', 'camapa', 'capima', 'car', 'cli', 'grucli', 'cligrucli', 'ope', 'tur', 'cob', 'comeve', 'con', 'decperope', 'lispre', 'tar', 'rec', 'hor', 'profuecir', 'proencir', 'grupro', 'detcob', 'opecaj', 'detopecaj', 'plazon', 'zon', 'entsal', 'enu', 'envinc', 'equgruproins', 'res', 'fac', 'fes', 'frahor', 'fratar', 'inc', 'inssis', 'lisnegmat', 'lisnegpro', 'manpro', 'remtarcre', 'opetarcre', 'parcon', 'paslispre', 'perope', 'polacc', 'regaud', 'regcon', 'regpreusu', 'remrecdom', 'traren', 'renpro', 'tarpro', 'tottur', 'traerrsis', 'vehcli', 'veropepro']
        tablas = ['cob', 'entsal', 'profuecir', 'regcon', 'tottur']
        
        for tabla in tablas:
            columnas = recupera_columnas(param, equinsa, tabla)

            """Genera un SELECT dinámico con las columnas dadas para obtener datos"""
            datos = obtener_datos_origen(param, equinsa, columnas, tabla)
            if datos:
                """Genera un SELECT dinámico con las columnas dadas"""
                insert_query = generar_insert(param, tabla, columnas)

                insert_datos(param, conn_mysql, tabla, insert_query, datos)
                conn_mysql.commit()

            time.sleep(10)
    
        print("✅ Inserción realizada")

    except Exception as e:
        param.error_sistema(e=e, debug="proceso.Exception")
        raise 

    finally:
        param.debug = "cierra conn"
        close_connection_mysql(conn_mysql, None)
    
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
    datos = []

    sql_query = f"SELECT count(*) FROM {tabla};"
    datos_equinsa = equinsa.execute_sql_command(sql_query)
    valor_str = datos_equinsa["rows"][0]["column1"]
    registros = int(valor_str) if int(valor_str) else 0

    if registros > 30000:
        datos = obtener_datos_origen_paginados(param, equinsa, columnas_str, tabla)
    else:
        sql_query = f"SELECT {columnas_str} FROM {tabla};"

        datos_equinsa = equinsa.execute_sql_command(sql_query)
        if datos_equinsa:
            datos = datos_equinsa["rows"]
        else:
            datos = []
    
    return datos        

# -------------------------------------------------------------------------------------------
def obtener_datos_origen_paginados(param: InfoTransaccion, equinsa, columnas_str, tabla):
    page_size = 10000
    page_number = 1
    param.debug = f"obtener_datos_origen_paginados {tabla}"
    datos = []

    while True:
        # Cálculo de OFFSET (SQL Server empieza en 0)
        offset = (page_number - 1) * page_size
    
        # Query con paginación
        sql_query = f"""SELECT {columnas_str} 
                        FROM {tabla}
                        ORDER BY 1,2,3,4  -- ¡Importante! Necesitas un campo para ordenar (ajústalo)
                        OFFSET {offset} ROWS
                        FETCH NEXT {page_size} ROWS ONLY;"""
        
        datos_equinsa = equinsa.execute_sql_command(sql_query)
        datos_pagina  = datos_equinsa.get("rows", []) if datos_equinsa else []
    
        if not datos_pagina:
            break

        datos.extend(datos_pagina)
        page_number += 1

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
def insert_datos(param: InfoTransaccion, conn_mysql, tabla, insert_query, datos_dict):
    """Ejecuta el INSERT en la base de datos MySQL destino"""
    param.debug = f"insertando en tabla: {tabla}"

    if datos_dict:
        datos_dict_ok = convertir_todo(datos_dict)
        columnas = list(datos_dict_ok[0].keys())
        datos = [tuple(row.get(col, None) for col in columnas) for row in datos_dict_ok]

        instruccion = insert_query.replace(", sql,", ", `sql`,")
        instruccion = instruccion.replace(", mod,", ", `mod`,")

        # Tamaño del lote (1000 registros por lote)
        tamano_lote = 1000

        cursor_mysql = conn_mysql.cursor(dictionary=True)
        # Insertar en lotes
        for i in range(0, len(datos), tamano_lote):
            lote = datos[i:i + tamano_lote]  # Obtener un lote de 1000 registros
            cursor_mysql.executemany(instruccion, lote)  # Insertar el lote
            conn_mysql.commit()  # Confirmar la transacción
            print(f"Insertados {len(lote)} registros. Total: {i + len(lote)}/{len(datos)}  en {tabla}")
        cursor_mysql.close()
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
        # print(f"Error convirtiendo fecha {fecha_str}: {e}")
        return fecha_str  # Devuelve la original si falla


def es_numero(valor):
    try:
        # Reemplazar coma por punto antes de validar
        valor = valor.replace(',', '.') if isinstance(valor, str) else valor
        float(valor)
        return True
    except (ValueError, TypeError):
        return False

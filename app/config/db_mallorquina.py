# Para MySql
import mysql.connector
from mysql.connector import Error

# Para SQL Server
import pyodbc

from sshtunnel import SSHTunnelForwarder


from app.config.settings import settings
from app.utils.utilidades import graba_log, imprime
from app.utils.InfoTransaccion import InfoTransaccion


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def get_db_connection_mysql():
    param = InfoTransaccion(debug=f"Conectando con: {settings.MYSQL_DB_HOST_MLL}/{settings.MYSQL_DB_PORT_MLL}/{settings.MYSQL_DB_USER_MLL}/{settings.MYSQL_DB_DATABASE_MLL}")

    try:
        if settings.SSH_CONEX:
            print("Tunel SSH")
            # Crear el túnel SSH
            with SSHTunnelForwarder(
                (settings.SSH_HOST, settings.SSH_PORT),
                ssh_username=settings.SSH_USER,
                ssh_password=settings.SSH_PWD,  # Usar contraseña en lugar de clave privada
                remote_bind_address=(settings.MYSQL_DB_HOST_MLL, settings.MYSQL_DB_PORT_MLL)
            ) as tunnel:
                print(f"""parametros: 
                          settings.SSH_HOST: {settings.SSH_HOST} 
                          settings.SSH_PORT: {settings.SSH_PORT} 
                          settings.SSH_USER: {settings.SSH_USER}  
                          y el Puerto local asignado (tunnel.local_bind_port): {tunnel.local_bind_port}
                          """)
                # Configuración de la conexión con mysql.connector
                connection = mysql.connector.connect(
                    host='127.0.0.1',  # Siempre localhost al usar el túnel
                    port= 3306, #tunnel.local_bind_port,
                    user=settings.MYSQL_DB_USER_MLL,
                    password=settings.MYSQL_DB_PWD_MLL,
                    database=settings.MYSQL_DB_DATABASE_MLL,
                    charset=settings.MYSQL_DB_CHARSET
                )
            print("Tunel SSH creado")
            
            # Prueba de conexión
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            print(f"Conectado a la base de datos: {result[0]}")
            x=1/0

        else:
            connection = mysql.connector.connect(
                host=settings.MYSQL_DB_HOST_MLL,
                port=settings.MYSQL_DB_PORT_MLL,
                user=settings.MYSQL_DB_USER_MLL,
                password= settings.MYSQL_DB_PWD_MLL,
                database=settings.MYSQL_DB_DATABASE_MLL,
                charset=settings.MYSQL_DB_CHARSET
            )

        # # Establecer explícitamente la collation en la conexión
        # connection.set_charset_collation('utf8mb4', 'utf8mb4_unicode_ci')
        # cursor = connection.cursor()
        # cursor.execute("SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';")

        # # Verificar collation
        # cursor.execute("SHOW VARIABLES LIKE 'collation_connection';")
        # print(cursor.fetchone())
        # cursor.close()

        return connection
    
    except Exception as e:
        param.error_sistema(e=e, debug="db_mallorquina.get_db_connection_mysql")
        raise

#----------------------------------------------------------------------------------------
def close_connection_mysql(conn, cursor):
    try:
        if conn is not None and conn.is_connected():
            if isinstance(cursor, mysql.connector.cursor.MySQLCursor):
                cursor.close()
            conn.close()
    
    except Error as e:
        raise 

#----------------------------------------------------------------------------------------
def get_db_connection_sqlserver(conexion_json):
    try:
        donde = "Inicio get_db_connection_sqlserver"
        conexion = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={conexion_json['host']},{conexion_json['port']};DATABASE={conexion_json['database']};UID={conexion_json['user']};PWD={conexion_json['password']}"
        donde = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={conexion_json['host']};DATABASE={conexion_json['database']};UID={conexion_json['user']};PWD='XXXXXXX'"
        connection =  pyodbc.connect(conexion)

        return connection
    
    except Exception as e:
        graba_log({"ret_code": -1, "ret_txt": "get_db_connection_sqlserver - "+ donde}, "Excepción", e)
        return False
    
#----------------------------------------------------------------------------------------
def close_connection_sqlserver(conn, cursor):
    try:
        if conn is not None:
            if cursor is not None:
                cursor.close()
            conn.close()
    
    except Error as e:
        return


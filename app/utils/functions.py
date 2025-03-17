from app.utils.InfoTransaccion import InfoTransaccion
from app.utils.mis_excepciones import MiException

# ------------------------------------------------------------------------------------------------
# Expande una lista que tenga dentro un elemento InfoTransaccion
# ------------------------------------------------------------------------------------------------
def expande_lista(lista:list) -> list:
        new_list = []

        for item in lista:
            if isinstance(item, InfoTransaccion):
                # Si el elemento es una instancia de InfoTransaccion, lo expandimos
                new_list.extend(item.to_list())
            else:
                # Si no, simplemente lo añadimos a la nueva lista
                new_list.append(item)

        return new_list



# ------------------------------------------------------------------------------------------------
# Convierte una fila pyodbc en un diccionario
# ------------------------------------------------------------------------------------------------
def row_to_dict(row, cursor):
    # print("Obtener los nombres de las columnas")
    columns = [column[0] for column in cursor.description]
    # print("columnas ", columns)

    # Combinar los nombres de las columnas con los valores del row
    datos = dict(zip(columns, row))
    # print("datos ", datos)
    return datos
    



# --------------------------------------------------------------------------------
# Control de autenticación de usuario
# --------------------------------------------------------------------------------
def control_usuario (param,  request):
    # Verificar la autenticación
    authenticated_user = request.state.user # AuthMiddleware.get_current_user(credentials)
    if param.user != authenticated_user:
        param.registrar_error(ret_txt="Error de usuario de conexión", ret_code = -1, debug = f"Error de usuario de conexión: {param.user} - {authenticated_user}")
        # yo no quiero generar un error..... param.sistem_error(txt_adic="Error de usuario", debug=f"{param.user} - {authenticated_user}")
        raise MiException(param,"Los usuarios no corresponden", -1)
    return True

# --------------------------------------------------------------------------------
# Control de autenticación de usuario


# este es si yo quisiera que en lugar de salirse con un Status 401, salga con un 200 y controlamos el error con ret_code


# --------------------------------------------------------------------------------
# def control_usuario (param,  request):
#     # Verificar la autenticación
#     authenticated_user = request.state.user # AuthMiddleware.get_current_user(credentials)
#     if param.user != authenticated_user:
#         param.registrar_error(ret_txt="Error de usuario de conexión", ret_code = -1, debug = f"Error de usuario de conexión: {param.user} - {authenticated_user}")
#         return False
#     return True


# --------------------------------------------------------------------------------
# Función para obtener el último cierre de caja de una tienda
# --------------------------------------------------------------------------------
def select_mysql(param: InfoTransaccion, conn_mysql, query: str, parametros: tuple = None, diccionario: bool = True) -> list:
    try:
        cursor_mysql = conn_mysql.cursor(dictionary=True)
        cursor_mysql.execute(query, parametros) 
        lista_bbdd = cursor_mysql.fetchall()
        cursor_mysql.close()

        return lista_bbdd
    
    except Exception as e:
        param.error_sistema(e=e, debug="select_mysql.Exception")
        raise 



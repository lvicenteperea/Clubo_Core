from datetime import datetime, timedelta
import json
import re
from fastapi import HTTPException

from app.utils.utilidades import graba_log, imprime

from app.models.mll_cfg_tablas import obtener_campos_tabla, crear_tabla_destino
from app.models.mll_cfg_bbdd import obtener_conexion_bbdd_origen
from app.config.db_mallorquina import get_db_connection_mysql, close_connection_mysql
from app.models.mll_cfg import obtener_cfg_general, actualizar_en_ejecucion

import app.services.mallorquina.sincroniza_tablas.proceso_general as proceso_general
import app.services.mallorquina.sincroniza_tablas.proceso_especifico as proceso_especifico
from app.utils.InfoTransaccion import InfoTransaccion
from app.utils.mis_excepciones import MiException

#----------------------------------------------------------------------------------------
# Este proceso se encarga de recorrer todas las tiendas y entidades y tablas que se van a tratar para sincronizar desde esas Tiendas/BBDD a la BBDD de La Mallorquina
# para ello:
#   - Recorre todas las tiendas activas: mll_cfg_bbdd.activo=S
#   - Recorre todas las entidades activas: mll_cfg_entidades.activo=S
#   - Recorre todas las tablas de cada entidad y para cada una de ellas:
#       - Si la tabla no tiene fecha de última actualización, se toma como fecha de última actualización la fecha 01/01/2025    
#       - Se calcula si se debe procesar en función de la diferencia entre la fecha de última actualización y la fecha actual
#       - Si se debe procesar, se ejecuta el proceso de sincronización
#       - Se actualiza la fecha de última actualización de la tabla
#----------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion) -> list:
    funcion = "sincroniza.proceso"
    param.debug = "Obtener Conf. Gen"
    resultado = []

    try:
        config = obtener_cfg_general(param)

        if not config.get("ID", False):
            param.sistem_error(txt_adic=f'No se han encontrado datos de configuración: config["En_Ejecucion"]', debug=f"{funcion}.config-ID")
            raise MiException(param,"No se han encontrado datos de configuración", -1)

        if config["En_Ejecucion"]:
            param.sistem_error(debug=f"{funcion}.config-en_ejecucion")
            raise MiException(param,"El proceso ya está en ejecución.", -1)

        param.debug = "actualiza ejec 1" 
        actualizar_en_ejecucion(param, 1)
        
        # -----------------------------------------------------------------------------------
        resultado = recorre_tiendas(param)
        # -----------------------------------------------------------------------------------

        param.debug = "Fin"
        return resultado
                  
    except MiException as e:
        param.error_sistema(e=e, debug="Sincroniza.Proceso.MiExcepcion")
        raise e
    except Exception as e:
        param.error_sistema(e=e, debug="Sincroniza.Proceso.Excepcion")
        raise e # HTTPException(status_code=500, detail=e)

    finally:
        actualizar_en_ejecucion(param, 0)

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def recorre_tiendas(param: InfoTransaccion) -> list:
    funcion = "sincroniza.recorre_tiendas"
    param.debug = "recorre_tiendas"
    resultado = []
    conn_mysql = None # para que no de error en el finally
    cursor_mysql = None # para que no de error en el finally

    try:

        param.debug = "conn. MySql"
        conn_mysql = get_db_connection_mysql()
        cursor_mysql = conn_mysql.cursor(dictionary=True)

        param.debug = "execute cfg_bbdd"
        cursor_mysql.execute("""SELECT a.ID, a.Nombre, a.Conexion, a.Ultima_Fecha_Carga
                                  FROM mll_cfg_bbdd a
                                 inner join mll_cfg_entidades b on a.id = b.id_bbdd and b.activo = 'S'
                                 where a.activo= 'S'""")
        lista_bbdd = cursor_mysql.fetchall()

        for bbdd in lista_bbdd:
            imprime([f"📚 Procesando BBDD(Tienda): {bbdd['ID']}-{bbdd['Nombre']}", f"Conexión: {json.loads(bbdd['Conexion'])['database']}", bbdd], "*")

            # ---------------------------------------------------------------------------------------
            param.debug = "por tablas"
            resultado.extend(recorre_entidades(param, bbdd, conn_mysql))
            # ---------------------------------------------------------------------------------------
            
            param.debug = "execute act. fec_Carga"
            cursor_mysql.execute(
                "UPDATE mll_cfg_bbdd SET Ultima_fecha_Carga = %s WHERE ID = %s",
                (datetime.now(), bbdd["ID"])
            )
        
        conn_mysql.commit()

        param.debug = "Fin"
        return resultado

                  
    except Exception as e:
        param.error_sistema(e=e, debug="sincroniza.recorretiendas.Excepcion")
        raise

    finally:
        close_connection_mysql(conn_mysql, cursor_mysql)

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def recorre_entidades(param: InfoTransaccion, tienda_bbdd, conn_mysql) -> list:
    funcion = "sincroniza.recorre_entidades"
    param.debug = "recorre_entidades"
    resultado = []
    cursor_mysql = None # para que no de error en el finally

    try:
        cursor_mysql = conn_mysql.cursor(dictionary=True)

        param.debug = "Select entidades"
        cursor_mysql.execute("SELECT * FROM mll_cfg_entidades WHERE id_bbdd = %s AND activo= 'S'", (tienda_bbdd['ID'],))

        lista_entidades = cursor_mysql.fetchall()

        for entidad in lista_entidades:
            imprime([f"📒 Procesando ENTIDAD:, {entidad['ID']}-{entidad['Nombre']}  -  stIdEnt: {entidad['stIdEnt']}", entidad], "-")
            
            # -------------------------------------------------------------------------
            param.debug = "por tablas"
            resultado.extend(recorre_tablas(param, tienda_bbdd["Nombre"], entidad, conn_mysql))
            # -------------------------------------------------------------------------

            param.debug = "execute act. fec_Carga"
            cursor_mysql.execute(
                "UPDATE mll_cfg_entidades SET Ultima_fecha_Carga = %s WHERE ID = %s",
                (datetime.now(), entidad["ID"])
            )
            
        conn_mysql.commit()

        param.debug = "Fin"
        return resultado

                  
    except Exception as e:
        param.error_sistema(e=e, debug="Sincroniza.recorre_entidades.excepcion")
        raise

    finally:
        if cursor_mysql is not None:
            cursor_mysql.close()


#----------------------------------------------------------------------------------------
# ejecutar_proceso: Sincroniza todas las tablas de una tienda. Recibe un json con los datos del registro de mll_cfg_bbdd:
#   - ID int: Es el ID de la tabla que vamos a tratar
#   - Nombre str: Es el nombre de la tienda
#   - Conexion str: es la conexión de la tienda en formato -->{"host": "ip", "port": "1433", "user": "usuario", "database": "nombre_database", "p a s  s w o  r d": "la_contraseña"}
#   - Ultima_Fecha_Carga str: fecha en la que se sincronizó la última vez
#----------------------------------------------------------------------------------------
def recorre_tablas(param: InfoTransaccion, nombre_bbdd, entidad, conn_mysql) -> list:
    resultado = []

    try:
        # ----------------------------------------------------------------------------------------------------
        # recogemos primero la configuración Tabla-Entidad
        param.debug = "Inicio"
        cursor_mysql = conn_mysql.cursor(dictionary=True)

        param.debug = "execute mll_cfg_tablas_entidades"
        cursor_mysql.execute("SELECT * FROM mll_cfg_tablas_entidades where id_entidad = %s",  (entidad["ID"],))
        tablas_entidad = cursor_mysql.fetchall()
        cursor_mysql.close()

        # ----------------------------------------------------------------------------------------------------
        # recogemos los datos de la tabla a tratar que vamos a tratar en el bucle
        param.debug = "Obtener cursor"
        # Obtener configuración y campos necesarios
        cursor_mysql = conn_mysql.cursor(dictionary=True)
        # ----------------------------------------------------------------------------------------------------

        for tabla in tablas_entidad:
            if tabla["Fecha_Ultima_Actualizacion"]:
                ultima_actualizacion = tabla["Fecha_Ultima_Actualizacion"] # Con el formato que viene no hace falta hacer datetime.strptime
            else:
                ultima_actualizacion = datetime.strptime("2025-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

            intervalo = tabla["Cada_Cuanto_Ejecutar"]
            procesar = (intervalo == 0 or (datetime.now() > ultima_actualizacion + timedelta(days=intervalo)))

            # imprime([f"{'NO ' if not procesar else ''}Procesando TABLA:", tabla, datetime.now(),  ultima_actualizacion, timedelta(days=intervalo), (intervalo == 0 or (datetime.now() > ultima_actualizacion + timedelta(days=intervalo)))], "-")
            if procesar: 
                # -----------------------------------------------------------------------------------------
                param.debug = "Select cfg_tablas"     # Obtener nombre de la tabla y si se debe borrar
                cursor_mysql.execute("SELECT * FROM mll_cfg_tablas WHERE ID = %s", (tabla["ID_Tabla"],))

                tabla_config = cursor_mysql.fetchone()
                # -----------------------------------------------------------------------------------------

                imprime([f"🔖 Procesando TABLA:", tabla_config["Tabla_Origen"], tabla, [datetime.now(),  ultima_actualizacion, timedelta(days=intervalo)]], "-")
                param.debug = f"Procesando tabla: {tabla}"

                # -----------------------------------------------------------------------------------------
                resultados = procesar_tabla(param, conn_mysql, entidad, tabla, tabla_config)
                resultado.append( {"nombre_bbdd": nombre_bbdd, 
                                   "entidad": entidad['Nombre'],
                                   "tabla_origen": tabla_config["Tabla_Origen"],
                                    "valor_max": resultados[0],
                                    "insertados": resultados[1],
                                    "actualizados": resultados[2],
                                    "error": resultados[3]
                                } )
                # -----------------------------------------------------------------------------------------
       
        return resultado

    except Exception as e:
        param.error_sistema(e=e, debug="Sincroniza.recorre_tablas.excepcion")
        raise 
            
    finally:
        if cursor_mysql is not None:
            cursor_mysql.close()



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def procesar_tabla(param: InfoTransaccion, conn_mysql, entidad, tabla, tabla_config) -> list:   # retorna  [valor_max, insertados, Actualizados]
    param.debug="Inicio"

    try:
        # nombre_tabla_origen = tabla_config["Tabla_Origen"]
        nombre_tabla_destino = tabla_config["Tabla_Destino"]

        param.debug = "obtener campos"
        # Obtener campos de la tabla
        campos = obtener_campos_tabla(conn_mysql, tabla["ID_entidad"],tabla["ID_Tabla"])

        param.debug = "crea_tabla_dest"
        # Crear tabla si no existe
        crear_tabla_destino(param, conn_mysql, nombre_tabla_destino, campos)

        param.debug = f'obt. Origen: {entidad["id_bbdd"]}' 
        bbdd_config = obtener_conexion_bbdd_origen(conn_mysql, entidad["id_bbdd"])   # Buscamos la conexión que necesitamos para esta bbdd origen
        if bbdd_config:
            # ----------------------------------------------------------------------------------------
            # Dependiendo de la tabla, se ejecuta un proceso u otro.
            # por un lado estan las tablas generales que se tratan de una forma 
            # y por otro las que tienen un tratamiento específico
            # ----------------------------------------------------------------------------------------
            if tabla_config["proceso_carga"]:
                resultados = proceso_especifico.proceso(param, conn_mysql, entidad, tabla, bbdd_config, campos, tabla_config)
            else:
                resultados = proceso_general.proceso(param, conn_mysql, entidad, tabla, bbdd_config, campos, tabla_config)
            # ----------------------------------------------------------------------------------------
        else:
            resultados = [0, 0, 0, "Sin conexión a la BBDD"]

        return resultados

    except Exception as e:
        param.error_sistema(e=e, debug="Sincroniza.procesar_tabla.excepción")
        raise 



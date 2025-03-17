import os
from datetime import datetime
import pandas as pd

from app.models.mll_cfg import obtener_cfg_general
from app.config.db_mallorquina import get_db_connection_mysql, close_connection_mysql
from app.services.auxiliares.sendgrid_service import enviar_email

from app.utils.mis_excepciones import MiException
from app.utils.utilidades import graba_log, imprime
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion) -> list:
    funcion = "carga_productos_erp.proceso"
    param.debug="Inicio"
    resultado = []

    try:
        config = obtener_cfg_general(param)

        if len(param.parametros) >= 1  and param.parametros[0]:
            excel = os.path.join(f"{settings.RUTA_DATOS}/erp", f"{param.parametros[0]}")

        else:
            param.registrar_error(ret_txt= "No ha llegado fichero origen para cargar", debug=f"{funcion}.sin parametro entrada")
            raise MiException(param = param)

        # Aquí va la lógica específica para cada bbdd
        resultado = carga(param, excel)

        return resultado

    except Exception as e:
        param.error_sistema(e=e, debug="proceso.Exception")
        raise 
        
    finally:
        enviar_email(config["Lista_emails"],
                     "Proceso finalizado",
                     "El proceso de carga ha terminado."
        )

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
def carga (param: InfoTransaccion, excel):
    param.debug = "carga_productos_erp.carga"
    insertados = 0
    modificados = 0
    eliminados = 0
    
    try:
        
        # # Leer el Excel
        # df = pd.read_excel(excel)
        # # Leer el Excel asegurando que todo se lea como texto
        df = pd.read_excel(excel, dtype=str, keep_default_na=False)


        param.debug = "get_db_connection_mysql"
        conn_mysql = get_db_connection_mysql()
        param.debug = "cursor_____"
        cursor = conn_mysql.cursor(dictionary=True)

        param.debug = "Mapeo"
        # Mapeo de columnas del Excel con los campos de la tabla
        mapping = {
            'Código': 'ID',
            'Nombre': 'nombre',
            'Código de barras': 'codigo_barras',
            'Composición_para_etiqueta': 'composicion_etiqueta',
            'Composición_completa': 'composicion_completa',
            'temporada': 'temporada',
            #'familia_cod': 'familia_cod',
            'Descripción': 'familia_desc',
            'grupo_de_carta': 'grupo_de_carta',
            'CENTRO PREPARACION CAFETERA': 'centro_preparacion_1',
            'CENTRO PREPARACION PLANCHA': 'centro_preparacion_2',
            'CENTRO PREPARACION COCINA': 'centro_preparacion_3',
            'alta_tpv': 'alta_tpv',
            'alta_glovo': 'alta_glovo',
            'alta_web': 'alta_web',
            'alta_catering': 'alta_catering',
            'Huevo': 'huevo',
            'Leche': 'leche',
            'Crustaceos': 'crustaceos',
            'Cáscara': 'cascara',
            'Gluten': 'gluten',
            'Pescado': 'pescado',
            'Altramuz': 'altramuz',
            'Mostaza': 'mostaza',
            'Cacahuetes': 'cacahuetes',
            'Apio': 'apio',
            'Sulfitos': 'sulfitos',
            'Soja': 'soja',
            'Moluscos': 'moluscos',
            'Sésamo': 'sesamo',
            'Población_diana': 'poblacion_diana',
            'Uso_esperado': 'uso_esperado',
            'Condiciones_almacenamiento': 'condiciones_almacenamiento',
            'Condiciones_conservación': 'condiciones_conservacion',
            'Vida_frío_desde_fabric.': 'vida_fri_desde_fabric',
            'Peso_neto_aprox': 'peso_neto_aprox',
            'Rec_Aerobios_totales': 'rec_aerobios_totales',
            'Rec_Enterobacterias': 'rec_enterobacterias',
            'Rec_Escherichia_Coli': 'rec_escherichia_coli',
            'Rec_Staphylococcus_Aureus': 'rec_staphylococcus_aureus',
            'Det_Salmonella_cpp': 'det_salmonella_cpp',
            'Rec_Listeria_Monocytogenes': 'rec_listeria_monocytogenes',
            'Rec_Mohos_y_levaduras': 'rec_mohos_y_levaduras',
            'Valor_energetico_Kcal_Kj': 'valor_energetico_kcal_kj',
            'Grasas_g': 'grasas_g',
            'De_las_cuales_SATURADAS_g': 'de_las_cuales_saturadas_g',
            'Hidratos_de_carbono_g': 'hidratos_de_carbono_g',
            'De_los_cuales_AZUCARES_g': 'de_los_cuales_azucares_g',
            'Proteinas_g': 'proteinas_g',
            'Sal_g': 'sal_g',
            'Fibra_dietetica_g': 'fibra_dietetica_g',
            'Otros': 'otros',
            'fec_modificacion': 'fec_modificacion'
        }

        # Procesar registros del Excel
        for x, row in df.iterrows():
            row = row.fillna('')  # Reemplazar valores NaN con cadenas vacías

            # imprime([row], "*")

            param.debug = f"Código: {row['Código']}"
            codigo = row['Código']

            param.debug = f"fec_modificacion: {row.get('fec_modificacion', None)}"
            if row['fec_modificacion']:
                param.debug = f"fec_modificacion1: {row.get('fec_modificacion', None)}"
                fec_modificacion = datetime.strptime(row.get('fec_modificacion', None), "%Y-%m-%d %H:%M:%S")
            else:
                param.debug = f"fec_modificacion2: {row.get('fec_modificacion', None)}"
                fec_modificacion = datetime.strptime('2020-01-01 01:01:01', "%Y-%m-%d %H:%M:%S")

            # Consultar si el producto ya existe
            param.debug = "select 1"
            cursor.execute("SELECT IF(fec_modificacion = '' OR fec_modificacion IS NULL, NOW(), STR_TO_DATE(fec_modificacion, %s)) as fec_modificacion_BBDD FROM erp_productos WHERE ID = %s", ('%Y-%m-%d %H:%i:%s', codigo,))
            resultado_dict = cursor.fetchone()

            if resultado_dict:
                for _, campo in resultado_dict.items():
                    param.debug = f"campo: {type(campo)}-{campo}"
                    fec_modificacion_BBDD = campo
                
                param.debug = f"fec_modificacion_BBDD: {type(fec_modificacion_BBDD)}-{fec_modificacion_BBDD}"
                if not fec_modificacion_BBDD:
                    fec_modificacion_BBDD = fec_modificacion

                param.debug = f"fec_modificacion_BBDD: {type(fec_modificacion_BBDD)}-{fec_modificacion_BBDD} - fec_modificacion: {type(fec_modificacion)}-{fec_modificacion}"
                # Actualizar si la fecha de modificación en el Excel es posterior
                if fec_modificacion and fec_modificacion > fec_modificacion_BBDD:
                    modificados += 1

                    param.debug = "update___"
                    campos = ', '.join(f"{v} = %s" for k, v in mapping.items() if k in row)
                    valores = tuple(row[k] for k in mapping.keys() if k in row) + (codigo,)
                    cursor.execute(f"UPDATE erp_productos SET {campos} WHERE ID = %s", valores)

                    # Procesar campos "pvp_*" para modificar en erp_productos_pvp
                    for col in row.index:
                        if col.startswith('pvp_') and row[col]:
                            id_bbdd, tipo = determinar_bbdd_y_tipo(col)
                            pvp = convertir_a_decimal(row[col])
                            # imprime([id_bbdd, tipo, pvp, col, row[col]], "=")
                            if pvp > 0:
                                param.debug = "insert/update 3___"
                                for x in range(0, len(id_bbdd)):
                                    cursor.execute(
                                        """INSERT INTO erp_productos_pvp (id_producto, id_BBDD, tipo, pvp)
                                                                  VALUES (%s, %s, %s, %s)
                                               ON DUPLICATE KEY UPDATE pvp = VALUES(pvp)""",
                                        (codigo, id_bbdd[x], tipo, pvp)
                                    )
                            else:
                                param.debug = "delete___"
                                for x in range(0, len(id_bbdd)):
                                    cursor.execute("""delete from erp_productos_pvp 
                                                       where id_producto = %s and id_BBDD = %s and tipo = %s""",
                                        (codigo, id_bbdd[x], tipo)
                                    )
                                eliminados += cursor.rowcount
            else:
                insertados += 1
                # Insertar nuevo registro
                param.debug = f"insert___ {x}" #{row}"
                columnas = ', '.join(mapping.values())
                marcadores = ', '.join(['%s'] * len(mapping))
                valores = tuple(row[k] if k in row else '' for k in mapping.keys())
                valores = tuple(elemento.replace("Si", "Sí") if isinstance(elemento, str) else elemento for elemento in valores)

                cursor.execute(f"INSERT INTO erp_productos ({columnas}) VALUES ({marcadores})", valores)

                # Procesar campos "pvp_*" para insertar en erp_productos_pvp
                for col in row.index:
                    if col.startswith('pvp_') and row[col]:
                        id_bbdd, tipo = determinar_bbdd_y_tipo(col)
                        pvp = convertir_a_decimal(row[col])
                        # imprime([id_bbdd, tipo, pvp, col, row[col]], "=")
                        param.debug = "insert 2___"
                        if pvp > 0:
                            for x in range(0, len(id_bbdd)):
                                cursor.execute("""INSERT INTO erp_productos_pvp (id_producto, id_BBDD, tipo, pvp)
                                                                         VALUES (%s, %s, %s, %s)""",
                                    (codigo, id_bbdd[x], tipo, pvp)
                                )

        # Confirmar transacciones y cerrar conexión
        conn_mysql.commit()

        return [f"Registros insertados: {insertados}",
                f"Registros modificados: {modificados}",
                f"Registros eliminados: {eliminados}"
               ]


    except Exception as e:
        param.error_sistema(e=e, debug="carga.Exception")
        raise 

    finally:
        close_connection_mysql(conn_mysql, cursor)


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
def determinar_bbdd_y_tipo(columna):
    mapping_bbdd_tipo = {
        # 'pvp_tienda_sol_quevedo': ([4, 5], 'Barra'),
        'pvp_tienda_sol_quevedo': ([4, 5], 'Comedor'),
        'pvp_terraza_quevedo': ([4], 'Terraza'),

        # 'pvp_tienda_velzquez_mg': ([1, 3, 6], 'Barra'),
        'pvp_tienda_velzquez_mg': ([1, 3, 6], 'Comedor'),

        # 'pvp_salon_sol': ([7], 'Barra'),
        'pvp_salon_sol': ([7], 'Comedor'),

        'pvp_web': ([91], 'Web'),
        'pvp_glovo': ([92], 'Glovo'),
        'pvp_catering': ([90], 'Catering')
    }
    return mapping_bbdd_tipo.get(columna, ([], ''))

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
def convertir_a_decimal(valor):
    try:
        return float(str(valor).replace(',', '.'))
    except ValueError:
        return 0.0



import pandas as pd
from datetime import datetime

from app.utils.utilidades import graba_log, imprime
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings


PATH: str = settings.RUTA_TPV # f"{settings.RUTA_DATOS}tarifas_a_TPV/"
# Definición de las tiendas y su correspondencia con id_bbdd
TIENDAS = {
    5: "Sol",
    4: "Quevedo",
    1: "Velazquez",
    6: "Moraleja",
    7: "Salon_SOL"
}

COLUMNAS_EXCEL = [
    "Id Plato", "Descripcion", "Barra", "Comedor", "Terraza", "Hotel",
    "Reservado", "Menú", "Orden Factura", "Orden Cocina", "OrdenTactil",
    "Grupo Carta 1", "Grupo Carta 2", "Grupo Carta 3", "Grupo Carta 4",
    "Familia", "Código Barras", "Centro", "Centro 2", "Centro 3"
]

# Consulta SQL para obtener los datos de ambas tablas
QUERY = """
SELECT p.ID AS 'Id Plato', 
    p.nombre AS 'Descripcion',
    p.codigo_barras AS 'Código Barras',
    p.grupo_de_carta AS 'Grupo Carta 1',
    p.centro_preparacion_1 AS 'Centro',
    p.centro_preparacion_2 AS 'Centro 2',
    p.centro_preparacion_3 AS 'Centro 3',
    pv.id_bbdd,
    pv.tipo,
    pv.pvp
FROM erp_productos p
LEFT JOIN erp_productos_pvp pv ON p.ID = pv.id_producto
WHERE pv.id_bbdd IN (1, 3, 4, 5, 6, 7)
and p.alta_tpv = "Sí"
"""


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion) -> list:
    resultado = []
    param.debug = "proceso"

    try:
        output_path = f"tarifas_{datetime.now().strftime('%Y%m%d%H%M%S')}_"

        df = obtener_datos(param)
        resultado = generar_excel(param, df, output_path)
        
        return resultado

    except Exception as e:
        param.error_sistema(e=e, debug="proceso.Exception")
        raise 
        

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
# Generar los archivos Excel por tienda
def generar_excel(param: InfoTransaccion, df, output_path: str) -> list:
    resultado = []
    error_log_path = f"{PATH}errores_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
    errores = []

    try:
        for id_bbdd, tienda in TIENDAS.items():
            df_tienda = df[df["id_bbdd"] == id_bbdd]
            total_filas = len(df_tienda)
            imprime([f"Tienda: {tienda} - Filas: {total_filas}"], "*")

            # Preparar datos para el archivo de cada tienda
            data = []
            for producto_id in df_tienda["Id Plato"].unique():
                producto = df_tienda[df_tienda["Id Plato"] == producto_id]

                barra = producto.loc[producto["tipo"] == "Barra", "pvp"].values[0] if "Barra" in producto["tipo"].values else ""
                comedor = producto.loc[producto["tipo"] == "Comedor", "pvp"].values[0] if "Comedor" in producto["tipo"].values else ""
                terraza = producto.loc[producto["tipo"] == "Terraza", "pvp"].values[0] if "Terraza" in producto["tipo"].values else ""

                # Si todas las columnas de precio están vacías, omitir el registro
                if not barra and not comedor and not terraza:
                    continue

                grupo_carta = producto.iloc[0]["Grupo Carta 1"]
                if pd.isna(grupo_carta) or grupo_carta == "":
                    errores.append(f"Producto {producto_id} de la tienda {tienda} no tiene Grupo Carta 1")
                    continue

                data.append([
                    producto.iloc[0]["Id Plato"],
                    producto.iloc[0]["Descripcion"],
                    barra, comedor, terraza,
                    "", "", "", "", "", "",
                    grupo_carta, "", "", "",
                    "", producto.iloc[0]["Código Barras"],
                    producto.iloc[0]["Centro"], producto.iloc[0]["Centro 2"], producto.iloc[0]["Centro 3"]
                ])

            filas = len(data)
            if filas == 0:
                print(f"No hay datos para la tienda {tienda}")
                resultado.append(f"No hay datos para la tienda {tienda}")
            else:
                # Crear DataFrame y exportar a Excel
                df_export = pd.DataFrame(data, columns=COLUMNAS_EXCEL)
                output_file = f"{output_path}{tienda}.xlsx"
                df_export.to_excel(f"{PATH}{output_file}", index=False)
                
                resultado.append({"fichero": f'{output_file}', "texto": f'{tienda}: {len(data)} precios de {total_filas}'})

        if errores:
            with open(error_log_path, "w") as error_file:
                for error in errores:
                    error_file.write(error + "\n")

        return resultado

    except Exception as e:
        param.error_sistema(e=e, debug="proceso.Exception")
        raise 
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
# Conectar a la base de datos y obtener los datos

from app.config.db_mallorquina import get_db_connection_mysql, close_connection_mysql

def obtener_datos(param: InfoTransaccion) -> pd.DataFrame:
    try: 
        param.debug = "obtener_datos"
        conn_mysql = get_db_connection_mysql()

        param.debug = "read_sql_query"
        df = pd.read_sql_query(QUERY, conn_mysql)

        conn_mysql.close()
        return df

    except Exception as e:
        param.error_sistema(e=e, debug="obtener_datos.Exception")
        raise 

    finally:
        close_connection_mysql(conn=conn_mysql, cursor=None)
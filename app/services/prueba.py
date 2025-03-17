import datetime
print(datetime.datetime(2055, 1, 1, 0, 0))




# l1= """[Id Plato], 
# [Orden Factura], Descripcion, Importe, Raciones, Peso, [Impuesto Incluido], [Total Base], [Total Impuesto], [Total Total], [Fecha Invitacion], [Id Relacion], [Serie Puesto Facturacion], Modo, [Fusion], Iva2Sn, Modo2, bPrimerCombinado, [Id Camarero], [Id Usuario], [Nombre Camarero], [Nombre Usuario], [Id Familia], [Des Familia], [Id SubFamilia], [Des SubFamilia], [Id Grupo], [Des Grupo], [Peso 100], [Dcto %], [Total Dcto], 
# Rac_Ini, 
# [Modo Botella], Refrescos, [Id Clase], 
# [Id Principal], 
# Fecha_Hora, 
# [Cantidad Receta], [Desc Cantidad], [Tipo Bono Tarjeta PP], [Id Tarjeta PP], 
# stIdEnt , {entidad['ID']}  as id_entidad"""
# l2= """Id_Plato, 
# Orden_Factura, Descripcion, Importe, Raciones, Peso, Impuesto_Incluido, Total_Base, Total_Impuesto, Total_Total, Fecha_Invitacion, Id_Relacion, Serie_Puesto_Facturacion, Modo, Fusion, Iva2Sn, Modo2, bPrimerCombinado, Id_Camarero, Id_Usuario, Nombre_Camarero, Nombre_Usuario, Id_Familia, Des_Familia, Id_SubFamilia, Des_SubFamilia, Id_Grupo, Des_Grupo, Peso_100, Dcto_pct, Total_Dcto,
# Rac_Ini, 
# Modo_Botella, Refrescos, Id_Clase, 
# Id_Principal,  
# Fecha_Hora, 
# Cantidad_Receta, Desc_Cantidad, Tipo_Bono_Tarjeta_PP, Id_Tarjeta_PP, 
# stIdEnt, id_entidad"""
# l3= "(stIdEnt, Id_Principal, Orden_Factura, Descripcion, Importe, Raciones, Peso, Impuesto_Incluido, Total_Base, Total_Impuesto, Total_Total, Fecha_Invitacion, Id_Relacion, Serie_Puesto_Facturacion, Modo, Fusion, Iva2Sn, Modo2, bPrimerCombinado, Id_Camarero, Id_Usuario, Nombre_Camarero, Nombre_Usuario, Id_Familia, Des_Familia, Id_SubFamilia, Des_SubFamilia, Id_Grupo, Des_Grupo, Peso_100, Dcto_pct, Total_Dcto, id_entidad, Modo_Botella, Refrescos, Id_Clase, Id_Plato, Rac_Ini, Cantidad_Receta, Desc_Cantidad, Tipo_Bono_Tarjeta_PP, Id_Tarjeta_PP, Fecha_Hora) "
# l4= "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# print(l1.count(','))
# print(l2.count(','))
# print(l3.count(','))
# print(l4.count(','))





# Datos:       (200004, 0, 'CROISSANT', Decimal('1.800'), Decimal('1.000'), Decimal('0.000'), True, Decimal('1.640'), Decimal('0.160'), Decimal('1.800'), None, 1158479, 'V1', 0, False, False, 0, False, 0, 2, '', 'CAMARERO = 1', 0, '', 0, '', 1, 'BOLLERIA', 0, Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), 0, Decimal('0.00'), 0, 2845056, datetime.datetime(2025, 2, 14, 8, 1, 46, 307000), Decimal('1.000'), '', 0, 0, '2202232042133764', 5)
# Convertidos: (200004, 0, 'CROISSANT', 1.8, 1.0, 0.0, 1, 1.64, 0.16, 1.8, None, 1158479, 'V1', 0, 0, 0, 0, 0, 0, 2, None, 'CAMARERO = 1', 0, None, 0, None, 1, 'BOLLERIA', 0, 0.0, 0.0, 0.0, 0, 0.0, 0, 2845056, '2025-02-14 08:01:46', 1.0, None, 0, 0, '2202232042133764', 5)
# INSERT: INSERT INTO TPV_FACTURAS_COMANDA (stIdEnt, Id_Principal, Orden_Factura, Descripcion, Importe, Raciones, Peso, Impuesto_Incluido, Total_BaseTotal_Impuesto, Total_Total, Fecha_Invitacion, Id_Relacion, Serie_Puesto_Facturacion, Modo, Fusion, Iva2Sn, Modo2, bPrimerCombinado, Id_Camarero, Id_Usuario, Nombre_Camarero, Nombre_Usuario, Id_Familia, Des_Familia, Id_SubFamilia, Des_SubFamilia, Id_Grupo, Des_Grupo, Peso_100, Dcto_pct, Total_Dcto, id_entidad, Modo_Botella, Refrescos, Id_Clase, Id_Plato, Rac_Ini, Cantidad_Receta, Desc_Cantidad, Tipo_Bono_Tarjeta_PP, Id_Tarjeta_PP, Fecha_Hora, Origen_BBDD)
#                                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);





# from datetime import datetime, timedelta


# columnas = [
#     "Fecha", "Hora_Cobro", "Tiempo", "Id_Salon", "Id_Mesa", "Comensales", "Tarifa", "Idioma", "Id_Turno", 
#     "Id_Camarero", "Id_Cliente_Habitacion", "Id_Apertura_Puesto_Cobro", "Factura_Num", "Iva_porc", "Descuento_porc", 
#     "Base", "Descuento", "Impuesto", "Total", "Propina", "Serie_Puesto_Facturacion", "Id_Relacion", "Id_Relacion_Cocina", 
#     "Recien_Abierta", "Bk", "Bk1", "Nombre_Cajero", "Anulada", "Fusion", "Base2", "Descuento2", "Iva2_porc", "Impuesto2", 
#     "Dcto_Manual", "Importe_Impresion", "Salida_Receta", "IdCobro_Propina", "Descripcion_Cobro_Propina", "lVeces_Impreso", 
#     "Edad", "VIdTipoCli", "IdEvento", "Factura_Num_Cliente", "Cocina_Evento", "Cocina_Pedido", "bDetenerComandaCocina_Mesa", 
#     "Cocina_Pedido_2", "CM_Id_Reserva", "CM_Id_Cliente", "Id_Envio_GS", "bEnviando", "Id_Envio_Realizado", "bNoCompCocina", "stIdEnt"
# ]

# datos = (datetime.datetime(2023, 7, 12, 8, 23, 2), None, datetime.datetime(2023, 7, 12, 8, 23, 2), 9, 218, 1, 1, 0, 1, 0, 81, 4614, 32725, 10.00, 0.00, 32.090, 0.000, 3.210, 35.300, 0.000, 'MN', 462640, 1883477, False, False, False, 'DIRECCION', False, False, 0.000, 0.000, 0.00, 0.00, False, 35.300, False, 0, '', 1, 0, 0, 0, 348, '', '', False, '', '', '', 0, False, 446, None, '1010221038290475')


# print("📌 Comparación de columnas y valores:")
# for i, (col, val) in enumerate(zip(columnas, datos[0])):
#     print(f"{i + 1}. {col}: {val}")

# # Si hay más valores en datos de los que hay en columnas
# if len(datos[0]) > len(columnas):
#     print("⚠️ Hay más valores en los datos que columnas en la consulta.")
# elif len(datos[0]) < len(columnas):
#     print("⚠️ Hay menos valores en los datos que columnas en la consulta.")
























# partes = "() () (1,2,3)".split(") (")
# parte3 = partes[2].strip("()")
# lista3_str = [item.strip().strip('"') for item in parte3.split(";")]
# print(lista3_str)

# lista3_str = [item.strip() for item in parte3.split(";")]
# print(lista3_str)




# def separar_cadena(cadena):
#     """
#     Recibe una cadena con dos partes entre paréntesis y devuelve dos listas:
#     - Una con los elementos de la primera parte.
#     - Otra con los elementos de la segunda parte.

#     :param cadena: Cadena en formato '(...) (...)'
#     :return: Dos listas, una para cada parte.
#     """
#     # Separar las dos partes
#     partes = cadena.split(") (")
#     if len(partes) != 2:
#         raise ValueError("La cadena debe contener dos partes separadas por ') ('.")
    
#     # Limpiar paréntesis iniciales y finales
#     parte1 = partes[0].strip("()")
#     parte2 = partes[1].strip("()")
    
#     # Convertir cada parte en listas separando por comas
#     lista1 = [item.strip().strip('"') for item in parte1.split(",")]
#     lista2 = [item.strip().strip('"') for item in parte2.split(",")]
    
#     return lista1, lista2




# cadena = '("stIdEnt", "Fecha", "[Serie Puesto Facturacion]", "[Factura Num]", "[Id Relacion]") ("{v1} >= \'{v2}\'", "{v1} >= CONVERT(DATETIME, \'{v2}\', 121) ", "{v1} >= \'{v2}\'", "{v1} >= {v2}", "{v1} >= {v2}")'

# # Llamar a la función
# lista1, lista2 = separar_cadena(cadena)

# # Mostrar resultados
# print("Lista 1:", lista1)
# print("Lista 2:", lista2)




# from cryptography.fernet import Fernet
# # Generar una nueva clave
# new_key = Fernet.generate_key()
# print(new_key.decode())  # Muestra la clave para configurarla como variable de entorno



# import secrets
# SECRET_KEY = secrets.token_hex(32)  # Genera una clave de 64 caracteres (32 bytes)
# print(SECRET_KEY)



# cadena = "Fecha, Hora_Cobro, Tiempo, Id_Salon, Id_Mesa, Comensales, Tarifa, Idioma, Id_Turno, Id_Camarero, Id_Cliente_Habitacion, Id_Apertura_Puesto_Cobro, Factura_Num, Iva_porc, Descuento_porc, Base, Descuento, Impuesto, Total, Propina, Serie_Puesto_Facturacion, Id_Relacion, Id_Relacion_Cocina, Recien_Abierta, Bk, Bk1, Nombre_Cajero, Anulada, Fusion, Base2, Descuento2, Iva2_porc, Impuesto2, Dcto_Manual, Importe_Impresion, Salida_Receta, IdCobro_Propina, Descripcion_Cobro_Propina, lVeces_Impreso, Edad, IdTipoCli, IdEvento, Factura_Num_Cliente, Cocina_Evento, Cocina_Pedido, bDetenerComandaCocina_Mesa, Cocina_Pedido_2, CM_Id_Reserva, CM_Id_Cliente, Id_Envio_GS, bEnviando, Id_Envio_Realizado, bNoCompCocina, stIdEnt, Origen_BBDD"
# elementos = len(cadena.split(","))
# print(elementos)
         


# cadena2 = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
# elementos = len(cadena2.split(","))
# print(elementos)


# cadena3 = "'datetime.datetime(2018)', None, 'datetime.datetime(2018)', 1, 1, 2, 0, 0, 1, 5, 0, 534, 1, Decimal('10.00')', Decimal('0.00')', Decimal('1.550')', Decimal('0.000')', Decimal('0.150')', Decimal('1.700')', Decimal('0.000')', 'T1', 1, 13, False, False, False, 'DIRECCION', False, False, Decimal('0.000')', Decimal('0.000')', Decimal('0.00')', Decimal('0.000')', False, Decimal('1.700')', False, 0, '', 1, 0, 0, 0, 0, '', '', False, '', '', '', 0, False, 1, None, '0610220837274849', 13"
# elementos = len(cadena3.split(","))
# print(elementos)






# import os

# def listar_archivos(directorio):
#     # Lista para almacenar los resultados
#     lista_archivos = []
    
#     # Recorrer el directorio y sus subdirectorios
#     for ruta_directorio, subdirs, archivos in os.walk(directorio):
#         for archivo in archivos:
#             # Generar la ruta completa del archivo
#             ruta_completa = os.path.join(ruta_directorio, archivo)
#             # Agregar el archivo con su ruta relativa
#             lista_archivos.append(f"{archivo}: {ruta_completa}")
    
#     # Ordenar la lista según la ruta completa
#     lista_archivos.sort(key=lambda x: x.split(": ", 1)[1])
    
#     return lista_archivos

# # Directorio raíz
# directorio_base = r"D:\Nube\GitHub\Mallorquina_API"

# # Obtener la lista de archivos
# archivos = listar_archivos(directorio_base)

# # Guardar los resultados en un archivo de texto o imprimirlos
# with open("lista_archivos.txt", "w", encoding="utf-8") as f:
#     for archivo in archivos:
#         f.write(archivo + "\n")

# # Mensaje de éxito
# print("Lista de archivos generada en 'lista_archivos.txt'")


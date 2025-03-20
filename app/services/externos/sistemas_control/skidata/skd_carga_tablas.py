from datetime import datetime
import time

from app.config.servicios_equinsa import EquinsaService

from app.utils.utilidades import graba_log, imprime
from app.config.db_clubo import get_db_connection_mysql, close_connection_mysql
from app.config.db_clubo import get_db_connection_sqlserver, close_connection_sqlserver
from app.utils.InfoTransaccion import InfoTransaccion
from app.config.settings import settings

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def proceso(param: InfoTransaccion) -> list:
    resultado = []
    param.debug = "proceso"
    # punto_venta = param.parametros[1]

    try:
        # Conectar a la base de datos
        conn_mysql = get_db_connection_mysql()
        

        bbdd_config = {"host": "192.168.17.99", "port": "1433", "user": "onlineuser", "database": "PARK_DB", "password": "Not4LocalUsers!"} # obtener_conexion_bbdd_origen(conn_mysql, ID_NUBE)
        param.debug = "conectamos con esta bbdd origen"
        conn_sqlserver = get_db_connection_sqlserver(bbdd_config)

        tablas = recupera_tablas(param,conn_sqlserver)
        
        for tabla in tablas:
            columnas = recupera_columnas(param, conn_sqlserver, tabla)

            """Genera un SELECT dinámico con las columnas dadas para obtener datos"""
            datos = obtener_datos_origen(param, conn_sqlserver, columnas, tabla)
            if datos:
                """Genera un SELECT dinámico con las columnas dadas"""
                insert_query = generar_insert(param, tabla, columnas)

                insert_datos(param, conn_mysql, tabla, insert_query, datos)
                conn_mysql.commit()

            # time.sleep(10)
    
        print("✅ Inserción realizada")

    except Exception as e:
        param.error_sistema(e=e, debug="proceso.Exception")
        raise 

    finally:
        param.debug = "cierra conn"
        close_connection_mysql(conn_mysql, None)
        close_connection_sqlserver(conn_sqlserver,  None)

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def recupera_tablas(param: InfoTransaccion, conn_sqlserver) -> list: 
    return ["BlockedContractParkingCardsSerialNumbers",    "APMCashBalance",    "APMCurrentCashBalance",    "BlockedContractParkerCards",    "CCMovements",    "CCOfContractParkersDueToExpire",    "CCSettlement",    "CCSettlementTotal",    "ContractParkerMovements",    "ContractParkingCards",    "ContractParkingCardsDueToExpire",    "CPCounting",    "CustomerLevelsPerCP",    "Customers",    "DefectiveContractParkingCards",    "ELPSettlement",    "EntriesExits",    "ExpiredContractParkingCards",    "ExtCardSystemMovements",    "LostContractParkingCards",    "MonetaryMovements",    "OpenParkingTrans",    "PaidExcessTimes",    "ParkingMovements",    "ParkingTransPartialRates",    "ParkingTransWithoutTurnover",    "PaymentWithISODiscountCard",    "PaymentWithSkiDataValueCard",    "PaymentWithSkiDataValueCardByEnCP",    "PaymentWithValidationProviders",    "PaystationCashBalance",    "PresentContractParkingCards",    "RentalAgmtsDueToExpire",    "Reservations",    "ReservationsEntered",    "ReservationsExpired",    "ReservationsOpen",    "ReservationsUsed",    "ReservationsWithOvertime",    "RevenueAmountCancellations",    "RevenueByEnCP",    "RevenueCashPayments",    "RevenueCashPaymentsByEnCP",    "RevenueCCPayments",    "RevenueCCPaymentsByEnCP",    "RevenueCheckPaymentsByEnCP",    "RevenueCreditEntriesIssued",    "RevenueCreditEntriesOnCreditCard",    "RevenueCreditEntriesRedeemed",    "RevenueELPPayments",    "RevenueELPPaymentsByEnCP",    "RevenueExtraCharges",    "RevenueInvoicePayments",    "RevenueInvoicePaymentsByEnCP",    "RevenueManualPaymentMethods",    "RevenueManualPaymentsByEnCP",    "RevenueParkingTrans",    "RevenueParkingTransSales",    "RevenuePaymentsByCheck",    "RevenueRoundingDifference",    "RevenueSales",    "Shifts",    "StatisticsCPCounting",    "StatisticsCustomerCounting",    "StatisticsCustomerCPCounting",    "StatisticsStoreyCounting",    "StoreyCounting",    "SystemEvents",    "TicketFlow",    "TicketFlowCharge",    "TotalCounter",    "TotalCounterSingleValues",    "Users",    "Respites",    "RevenueRespitesGranted",    "RevenueRespitesPaid",    "SystemInformation",    "RevenueCCPaymentsParkingTransSales",    "LogCCSettlement",    "LogELPSettlement",    "LogArchive",    "LogActivities",    "LogMauTransfer",    "RevenueInvoiceSales",    "ActiveContractParkingCards",    "ReservationsClosed",    "RevenuePayments",    "RevenuePaymentsByEnCP",    "ValidationProviders",    "CCDefinitions",    "ContractParkingCardsSerialNumbers",    "LogChange",    "PresentExtCardSystemCards",    "SPTPaymentWithValidationProviders",    "DeviceStatus",    "ExtCardSystemWhitelist",    "ExtCardSystemBlacklist",    "DevicesNotReady",    "SystemText",    "QuotaArticle",    "RevenueParkingTransExt",    "RevenueElectricCharging",    "Movements"  ]
    
# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def recupera_columnas(param: InfoTransaccion, conn_sqlserver, tabla: str) -> list: 
    param.debug = f"recupera_columnas {tabla}"
    sql_query = f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name = '{tabla}' ORDER BY ORDINAL_POSITION"

    cursor_sqlserver = conn_sqlserver.cursor()
    cursor_sqlserver.execute(sql_query)
    resultado = cursor_sqlserver.fetchall()
    cursor_sqlserver.close()

    columnas = [sublista[0] for sublista in resultado]

    return columnas

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def obtener_datos_origen(param: InfoTransaccion, conn_sqlserver, columnas, tabla):
    param.debug = f"obtener_datos_origen {tabla}"
    columnas_str = ", ".join(columnas)
    sql_query = f"SELECT {columnas_str} FROM {tabla};"

    cursor_sqlserver = conn_sqlserver.cursor()
    cursor_sqlserver.execute(sql_query)
    datos_skidata = cursor_sqlserver.fetchall()
    cursor_sqlserver.close()

    datos = [list(tupla) for tupla in datos_skidata]

    return datos        

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def generar_insert(param: InfoTransaccion, tabla, columnas):
    param.debug = f"generar_insert {tabla}"
    """Genera una sentencia INSERT INTO con los valores extraídos"""
    columnas_str = ", ".join(columnas)
    placeholders = ", ".join(["%s"] * len(columnas))  # Placeholders para evitar inyección SQL
    insert_query = f"INSERT INTO skd_{tabla} ({columnas_str}) VALUES ({placeholders})"

    return insert_query


# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def insert_datos(param: InfoTransaccion, conn_mysql, tabla, insert_query, datos_dict):
    """Ejecuta el INSERT en la base de datos MySQL destino"""
    param.debug = f"insertando en tabla: {tabla}"

    if datos_dict:
        datos_dict_ok = convertir_todo(datos_dict)
        columnas = datos_dict_ok # list(datos_dict_ok[0].keys())
        datos = columnas # [tuple(row.get(col, None) for col in columnas) for row in datos_dict_ok]

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
        for index, value in enumerate(row):
            if isinstance(value, str) and "/" in value and (len(value)==10 or len(value)==19):
                row[index] = convertir_fecha(value)
            elif es_numero(value):
                row[index] = value.replace(',', '.') if isinstance(value, str) else value

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

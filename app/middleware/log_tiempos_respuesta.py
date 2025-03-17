from fastapi import FastAPI, Request
import time
# import logging
from app.utils.utilidades import graba_log_info, imprime

# Configuración básica de logging
# print("inciando loger tiempos respuesa: logger = logging.getLogger('tiempo_respuesta')")
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("tiempo_respuesta")

app = FastAPI()

@app.middleware("http")
async def log_tiempos_respuesta(request: Request, call_next):
    # Middleware para registrar los tiempos de entrada, salida y duración total de cada solicitud.

    # Registrar el tiempo de entrada
    start_time = time.time()

    # Obtener información adicional
    ip = request.client.host  # IP del cliente
    servicio = request.url.path  # Ruta del endpoint llamado
    usuario = request.headers.get('X-User')  # Cambiar 'X-User' según tu sistema de autenticación


    # Registrar la solicitud (opcional)
    # logger.info(f"Solicitud entrante: {request.method} {request.url}")

    # Llamar al siguiente middleware o endpoint
    response = await call_next(request)

    # Registrar el tiempo de salida
    end_time = time.time()

    # Calcular la diferencia de tiempo en milisegundos
    duration = (end_time - start_time) * 1000

    try:
        body = await response.body() if hasattr(response, "body") else "No body available"
        graba_log_info(
            f"Tiempo de entrada: {start_time:.4f} ms, "
            f"Tiempo de salida: {end_time:.4f} ms, "
            f"Duración total: {duration:.2f} ms - "
            f"IP: {ip} - "
            f"Servicio: {servicio} - "
            f"Usuario: {usuario or 'No especificado'} - "
            f"Estado: {response.status_code} - "
            f"Respuesta: {body}"
        )

    except Exception as e:
        # graba_log_error(f"Error al registrar los logs: {str(e)}")
        print("graba_log_error(f'Error al registrar los logs: {str(e)}')")
    
    return response

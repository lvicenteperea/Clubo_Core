from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

logger = logging.getLogger("uvicorn")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url}")

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Processed in {process_time:.4f} seconds")

        return response

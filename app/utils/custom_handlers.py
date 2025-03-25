from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    detalles = []

    for err in errors:
        detalles.append({
            "campo": err.get("loc", []),
            "mensaje": err.get("msg"),
            "tipo": err.get("type")
        })

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Error de validación", "detalles": detalles}
    )

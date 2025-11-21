from fastapi import FastAPI

from core.config import settings
from core.database import Base, engine
from middleware.cors import add_cors_middleware
from middleware.security import add_security_middleware
from routers.public import general
from routers.private import aire, agua, estaciones, entidades_agua, metricas

# Crear tablas si no existen (comentar en producción para mejor performance)
# Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.api_name,
    version=settings.api_version,
    description=settings.api_description,
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # No expandir modelos por defecto
        "defaultModelExpandDepth": -1,   # No expandir detalles de modelos
        "displayRequestDuration": True,  # Mostrar duración de requests
        "tryItOutEnabled": True,         # Habilitar try it out
        "filter": True                   # Habilitar filtro de endpoints
    }
)

# Agregar middleware
add_cors_middleware(app)
add_security_middleware(app)

# Incluir routers públicos
app.include_router(
    general.router,
    prefix="/api/public"
)

# Incluir routers privados
app.include_router(
    aire.router,
    prefix="/api/private"
)

app.include_router(
    agua.router,
    prefix="/api/private"
)

app.include_router(
    estaciones.router,
    prefix="/api/private"
)

app.include_router(
    entidades_agua.router,
    prefix="/api/private"
)

app.include_router(
    metricas.router,
    prefix="/api/private"
)

# Ruta raíz
@app.get("/")
async def root():
    return {
        "message": "Observatorio Ambiental API",
        "version": settings.api_version,
        "docs": "/docs"
    }
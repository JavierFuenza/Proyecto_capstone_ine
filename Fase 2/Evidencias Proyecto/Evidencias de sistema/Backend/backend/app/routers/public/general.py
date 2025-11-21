from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from core.dependencies import get_db
from core.config import settings
from schemas.common import HealthResponse, InfoResponse

router = APIRouter(
    prefix="",
    tags=["Público"]
)

@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check básico de la API"""
    try:
        # Verificar conexión a la base de datos
        result = db.execute("SELECT 1").scalar()
        db_status = "connected" if result == 1 else "disconnected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat() + "Z",
        "database": db_status,
        "version": settings.api_version
    }

@router.get("/info", response_model=InfoResponse)
async def get_api_info():
    """Información general de la API"""
    return {
        "api_name": settings.api_name,
        "version": settings.api_version,
        "description": settings.api_description,
        "modules": ["agua", "aire"],
        "data_sources": [
            "Dirección General de Aguas (DGA)",
            "Sistema de Información Nacional de Calidad del Aire (SINCA)"
        ],
        "contact": {
            "email": settings.contact_email,
            "documentation": "/docs"
        }
    }
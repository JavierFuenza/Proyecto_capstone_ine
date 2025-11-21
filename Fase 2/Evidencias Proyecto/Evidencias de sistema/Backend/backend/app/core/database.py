from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Crear engine con configuración optimizada para performance
engine = create_engine(
    settings.database_url,
    pool_pre_ping=False,     # Desactivar para mejor performance
    pool_recycle=3600,       # Recicla conexiones cada 1 hora
    pool_size=10,            # Pool de conexiones más grande
    max_overflow=20,         # Conexiones adicionales si se necesitan
    pool_timeout=5,          # Timeout más corto
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class para modelos
Base = declarative_base()
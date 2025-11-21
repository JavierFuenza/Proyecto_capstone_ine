from sqlalchemy.orm import Session
from .database import SessionLocal

def get_db():
    """Dependencia para obtener sesión de base de datos optimizada"""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
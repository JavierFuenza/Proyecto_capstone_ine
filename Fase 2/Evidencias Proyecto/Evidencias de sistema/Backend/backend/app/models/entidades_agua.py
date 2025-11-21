from sqlalchemy import Column, BigInteger, Text
from core.database import Base

class EntidadAgua(Base):
    __tablename__ = "v_entidades_agua"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True)
    nombre = Column(Text)
    tipo = Column(Text)
    descripcion = Column(Text)

from sqlalchemy import Column, BigInteger, Text, Float
from core.database import Base

class Estacion(Base):
    __tablename__ = "v_estaciones"
    __table_args__ = {"schema": "public"}

    nombre = Column(Text, primary_key=True)
    latitud = Column(Float)
    longitud = Column(Float)
    numero_region = Column(BigInteger)
    nombre_region = Column(Text)
    descripcion = Column(Text)

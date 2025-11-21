from pydantic import BaseModel, Field
from typing import Optional

class EntidadAguaBase(BaseModel):
    nombre: str = Field(..., description="Nombre de la entidad de agua")
    tipo: str = Field(..., description="Tipo: estacion, cuenca, embalse, etc.")
    descripcion: Optional[str] = Field(None, description="Descripción de la entidad")

class EntidadAguaSchema(EntidadAguaBase):
    id: int

    class Config:
        from_attributes = True

class EntidadAguaCreate(EntidadAguaBase):
    """Schema para crear nuevas entidades de agua"""
    pass

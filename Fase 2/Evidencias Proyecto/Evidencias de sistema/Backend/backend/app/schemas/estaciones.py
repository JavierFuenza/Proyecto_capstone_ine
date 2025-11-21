from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class EstacionBase(BaseModel):
    nombre: str = Field(..., description="Nombre de la estación")
    latitud: Optional[float] = Field(None, description="Latitud en formato decimal")
    longitud: Optional[float] = Field(None, description="Longitud en formato decimal")
    numero_region: Optional[int] = Field(None, description="Número de la región (1-16)")
    nombre_region: Optional[str] = Field(None, max_length=100, description="Nombre de la región")
    descripcion: Optional[str] = Field(None, description="Descripción de la estación")

class EstacionSchema(EstacionBase):
    class Config:
        from_attributes = True

class EstacionCreate(EstacionBase):
    """Schema para crear nuevas estaciones (si lo necesitas en el futuro)"""
    pass

class RegionSchema(BaseModel):
    numero_region: int = Field(..., description="Número de la región")
    nombre_region: str = Field(..., description="Nombre de la región")

    class Config:
        from_attributes = True

class EstacionMetricasSchema(BaseModel):
    nombre: str = Field(..., description="Nombre de la estación")
    descripcion: Optional[str] = Field(None, description="Descripción de la estación")
    metricas_disponibles: List[str] = Field(..., description="Lista de categorías de métricas disponibles")

    class Config:
        from_attributes = True

class EstacionSubmetricasSchema(BaseModel):
    nombre: str = Field(..., description="Nombre de la estación")
    metrica: str = Field(..., description="Categoría de métrica consultada")
    submetricas_disponibles: List[str] = Field(..., description="Lista de submmétricas específicas disponibles")

    class Config:
        from_attributes = True

class RegistroSubmetricaSchema(BaseModel):
    periodo: str = Field(..., description="Mes o año del registro (ej: '2023-01' o '2023')")
    valor: Optional[float] = Field(None, description="Valor de la submétrica")

class DatosSubmetricaSchema(BaseModel):
    nombre: str = Field(..., description="Nombre de la estación")
    submetrica: str = Field(..., description="Nombre de la submétrica consultada")
    datos: List[RegistroSubmetricaSchema] = Field(..., description="Lista de registros históricos")

    class Config:
        from_attributes = True

class MetricasDetalladasSchema(BaseModel):
    temperatura: bool = Field(default=False)
    humedad_radiacion_uv: bool = Field(default=False)
    contaminantes: List[str] = Field(default_factory=list, description="Lista de contaminantes específicos: mp25, mp10, o3, so2, no2, co")

class EstacionConMetricasSchema(BaseModel):
    nombre: str = Field(..., description="Nombre de la estación")
    latitud: Optional[float] = Field(None, description="Latitud en formato decimal")
    longitud: Optional[float] = Field(None, description="Longitud en formato decimal")
    numero_region: Optional[int] = Field(None, description="Número de la región (1-16)")
    nombre_region: Optional[str] = Field(None, max_length=100, description="Nombre de la región")
    descripcion: Optional[str] = Field(None, description="Descripción de la estación")
    metricas_disponibles: List[str] = Field(..., description="Lista de categorías de métricas disponibles")
    metricas_detalladas: MetricasDetalladasSchema = Field(..., description="Detalle específico de cada métrica")

    class Config:
        from_attributes = True

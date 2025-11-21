from pydantic import BaseModel
from typing import Optional

# ============================
# Schemas para Temperatura
# ============================
class TemperaturaData(BaseModel):
    mes: str
    estacion: str
    temp_max_absoluta: Optional[float]
    temp_min_absoluta: Optional[float]
    temp_max_med: Optional[float]
    temp_min_med: Optional[float]
    temp_med: Optional[float]

    class Config:
        from_attributes = True

# ============================
# Schemas para Humedad, Radiación y UV
# ============================
class HumedadRadiacionUVData(BaseModel):
    mes: str
    estacion: str
    humedad_rel_med_mens: Optional[float]
    rad_global_med: Optional[int]
    uvb_prom: Optional[float]

    class Config:
        from_attributes = True

# ============================
# Schemas para Olas de Calor
# ============================
class OlasDeCalorData(BaseModel):
    mes: str
    estacion: str
    num_eventos_de_olas_de_calor: Optional[int]

    class Config:
        from_attributes = True

# ============================
# Schemas para Contaminantes - Datos Anuales
# ============================
class ContaminanteAnualData(BaseModel):
    anio: int
    estacion: str
    max_hor_anual: Optional[float]
    min_hor_anual: Optional[float]
    perc50: Optional[float]
    perc90: Optional[float]
    perc95: Optional[float]
    perc98: Optional[float]
    perc99: Optional[float] = None

    class Config:
        from_attributes = True

# ============================
# Schemas para Contaminantes - Datos Mensuales
# ============================
class ContaminanteMensualData(BaseModel):
    mes: str
    estacion: str
    med_mens: Optional[float]

    class Config:
        from_attributes = True

# ============================
# Schema de Respuesta Completa por Métrica
# ============================
class MetricaResponse(BaseModel):
    metrica: str
    estacion: str
    tiene_datos: bool
    datos_mensuales: list = []
    datos_anuales: list = []

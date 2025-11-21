from pydantic import BaseModel
from typing import Optional
from .common import BaseResponse

# ============================
# Esquemas para Vistas - Aire
# ============================

class TemperaturaSchema(BaseResponse):
    mes: str
    estacion: str
    temp_max_absoluta: Optional[float]
    temp_min_absoluta: Optional[float]
    temp_max_med: Optional[float]
    temp_min_med: Optional[float]
    temp_med: Optional[float]

class HumedadRadiacionUVSchema(BaseResponse):
    mes: str
    estacion: str
    humedad_rel_med_mens: Optional[float]
    rad_global_med: Optional[float]
    uvb_prom: Optional[float]

class Mp25AnualSchema(BaseResponse):
    anio: int
    estacion: str
    mp25_max_hor_anual: Optional[float]
    mp25_min_hor_anual: Optional[float]
    mp25_perc50: Optional[float]
    mp25_perc90: Optional[float]
    mp25_perc95: Optional[float]
    mp25_perc98: Optional[float]

class Mp25MensualSchema(BaseResponse):
    mes: str
    estacion: str
    mp25_med_mens: Optional[float]

class Mp10AnualSchema(BaseResponse):
    anio: int
    estacion: str
    mp10_max_hor_anual: Optional[float]
    mp10_min_hor_anual: Optional[float]
    mp10_perc50: Optional[float]
    mp10_perc90: Optional[float]
    mp10_perc95: Optional[float]
    mp10_perc98: Optional[float]

class Mp10MensualSchema(BaseResponse):
    mes: str
    estacion: str
    mp10_med_mens: Optional[int]

class O3AnualSchema(BaseResponse):
    anio: int
    estacion: str
    o3_max_hor_anual: Optional[float]
    o3_min_hor_anual: Optional[int]
    o3_perc50: Optional[float]
    o3_perc90: Optional[float]
    o3_perc95: Optional[float]
    o3_perc98: Optional[float]
    o3_perc99: Optional[float]

class O3MensualSchema(BaseResponse):
    mes: str
    estacion: str
    o3_med_mens: Optional[float]

class So2AnualSchema(BaseResponse):
    anio: int
    estacion: str
    so2_max_hor_anual: Optional[float]
    so2_min_anual: Optional[float]
    so2_perc50: Optional[float]
    so2_perc90: Optional[float]
    so2_perc95: Optional[float]
    so2_perc98: Optional[float]
    so2_perc99: Optional[float]

class So2MensualSchema(BaseResponse):
    mes: str
    estacion: str
    so2_med_mens: Optional[float]

class No2AnualSchema(BaseResponse):
    anio: int
    estacion: str
    no2_max_hor_anual: Optional[float]
    no2_min_hor_anual: Optional[float]
    no2_perc50: Optional[float]
    no2_perc90: Optional[float]
    no2_perc95: Optional[float]
    no2_perc98: Optional[float]
    no2_perc99: Optional[float]

class No2MensualSchema(BaseResponse):
    mes: str
    estacion: str
    no2_med_mens: Optional[float]

class CoAnualSchema(BaseResponse):
    anio: int
    estacion: str
    co_max_hor_anual: Optional[float]
    co_min_hor_anual: Optional[float]
    co_perc50: Optional[float]
    co_perc90: Optional[float]
    co_perc95: Optional[float]
    co_perc98: Optional[float]
    co_perc99: Optional[float]

class CoMensualSchema(BaseResponse):
    mes: str
    estacion: str
    co_med_mens: Optional[float]

class NoAnualSchema(BaseResponse):
    anio: int
    estacion: str
    no_max_hor_anual: Optional[float]
    no_min_hor_anual: Optional[float]
    no_perc50: Optional[float]
    no_perc90: Optional[float]
    no_perc95: Optional[float]
    no_perc98: Optional[float]
    no_perc99: Optional[float]

class NoMensualSchema(BaseResponse):
    mes: str
    estacion: str
    no_med_mens: Optional[float]

class NoxAnualSchema(BaseResponse):
    anio: int
    estacion: str
    nox_max_hor_anual: Optional[float]
    nox_min_hor_anual: Optional[float]
    nox_perc50: Optional[float]
    nox_perc90: Optional[float]
    nox_perc95: Optional[float]
    nox_perc98: Optional[float]
    nox_perc99: Optional[float]

class NoxMensualSchema(BaseResponse):
    mes: str
    estacion: str
    nox_med_mens: Optional[float]

class OlasCalorSchema(BaseResponse):
    mes: str
    estacion: str
    num_eventos_de_olas_de_calor: Optional[int]

class EstacionesSchema(BaseResponse):
    nombre: str
    latitud: Optional[float]
    longitud: Optional[float]
    numero_region: Optional[int]
    nombre_region: Optional[str]
    descripcion: Optional[str]
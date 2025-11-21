from pydantic import BaseModel
from typing import Optional
from .common import BaseResponse

# ============================
# Esquemas para Vistas - Agua
# ============================

class MarMensualSchema(BaseResponse):
    mes: str
    estacion: str
    temp_superficial_del_mar: Optional[float]
    nivel_medio_del_mar: Optional[float]

class GlaciaresAnualCuencaSchema(BaseResponse):
    anio: int
    estacion: str  # Cambio: en el esquema se llama "estacion" no "cuenca"
    num_glaciares_por_cuenca: Optional[int]
    superficie_de_glaciares_por_cuenca: Optional[float]
    volumen_de_hielo_glaciar_estimado_por_cuenca: Optional[float]
    volumen_de_agua_de_glaciares_estimada_por_cuenca: Optional[float]

# ============================
# Esquemas para Vistas - Solo campos esenciales
# ============================

class ColiformesBiologicaSchema(BaseResponse):
    dia: str
    estaciones_poal: str
    value: Optional[int]

class ColiformesAcuosaSchema(BaseResponse):
    dia: str
    estaciones_poal: str
    value: Optional[float]

class MetalesSedimentariaSchema(BaseResponse):
    dia: str
    estaciones_poal: str
    parametros_poal: str
    value: Optional[float]

class MetalesAcuosaSchema(BaseResponse):
    dia: str
    estaciones_poal: str
    parametros_poal: str
    value: Optional[float]

class CaudalSchema(BaseResponse):
    mes: str
    aguas_corrientes: str
    estaciones_fluviometricas: str
    value: Optional[float]

class LluviaSchema(BaseResponse):
    mes: str
    estaciones_meteorologicas_dmc: str
    value: Optional[float]

class EvaporacionSchema(BaseResponse):
    mes: str
    estacion: str
    value: Optional[float]

class EmbalseSchema(BaseResponse):
    mes: str
    embalse: str
    value: Optional[float]

class NieveSchema(BaseResponse):
    dia: str
    estaciones_nivometricas: str
    value: Optional[int]

class PozoSchema(BaseResponse):
    dia: str
    estaciones_pozo: str
    value: Optional[float]

class EntidadesAguaSchema(BaseResponse):
    id: int
    nombre: Optional[str]
    tipo: Optional[str]
    descripcion: Optional[str]
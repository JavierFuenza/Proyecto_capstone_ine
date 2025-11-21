from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.dependencies import get_db
from models.aire import *
from schemas.aire import *

# Crear sub-routers para organizar endpoints
general_router = APIRouter(
    prefix="/aire/climaticos",
    tags=["Aire - Climáticos"],
    responses={404: {"description": "No encontrado"}}
)

mp25_router = APIRouter(
    prefix="/aire/mp25",
    tags=["Aire - MP2.5"],
    responses={404: {"description": "No encontrado"}}
)

mp10_router = APIRouter(
    prefix="/aire/mp10",
    tags=["Aire - MP10"],
    responses={404: {"description": "No encontrado"}}
)

o3_router = APIRouter(
    prefix="/aire/o3",
    tags=["Aire - Ozono (O3)"],
    responses={404: {"description": "No encontrado"}}
)

so2_router = APIRouter(
    prefix="/aire/so2",
    tags=["Aire - Dióxido de Azufre (SO2)"],
    responses={404: {"description": "No encontrado"}}
)

no2_router = APIRouter(
    prefix="/aire/no2",
    tags=["Aire - Dióxido de Nitrógeno (NO2)"],
    responses={404: {"description": "No encontrado"}}
)

co_router = APIRouter(
    prefix="/aire/co",
    tags=["Aire - Monóxido de Carbono (CO)"],
    responses={404: {"description": "No encontrado"}}
)

no_router = APIRouter(
    prefix="/aire/no",
    tags=["Aire - Óxido de Nitrógeno (NO)"],
    responses={404: {"description": "No encontrado"}}
)

nox_router = APIRouter(
    prefix="/aire/nox",
    tags=["Aire - Óxidos de Nitrógeno (NOx)"],
    responses={404: {"description": "No encontrado"}}
)

eventos_router = APIRouter(
    prefix="/aire/eventos",
    tags=["Aire - Eventos Climáticos"],
    responses={404: {"description": "No encontrado"}}
)

# Router principal para incluir en main.py
router = APIRouter()

# ============================
# ENDPOINTS - CLIMÁTICOS
# ============================

@general_router.get(
    "/temperatura",
    response_model=List[TemperaturaSchema],
    summary="Obtener datos de temperatura",
    description="Retorna todas las mediciones de temperatura registradas en las estaciones meteorológicas de Chile."
)
async def get_temperatura(db: Session = Depends(get_db)):
    """
    Obtiene datos mensuales de temperatura por estación meteorológica.

    **Datos incluidos:**
    - Temperatura máxima absoluta (°C)
    - Temperatura mínima absoluta (°C)
    - Temperatura máxima media (°C)
    - Temperatura mínima media (°C)
    - Temperatura media (°C)

    **Periodo:** Datos históricos desde 1981 hasta la actualidad

    **Fuente:** Estaciones meteorológicas DMC (Dirección Meteorológica de Chile)
    """
    data = db.query(VTemperatura).order_by(VTemperatura.mes).all()
    return data

@general_router.get(
    "/humedad-radiacion-uv",
    response_model=List[HumedadRadiacionUVSchema],
    summary="Obtener datos de humedad y radiación",
    description="Retorna datos de humedad relativa, radiación global y radiación UVB por estación."
)
async def get_humedad_radiacion_uv(db: Session = Depends(get_db)):
    """
    Obtiene datos mensuales de humedad relativa y radiación solar.

    **Datos incluidos:**
    - Humedad relativa media (%)
    - Radiación global media (W/m²)
    - Radiación UVB media (W/m²)

    **Periodo:** Datos históricos desde 2010 hasta la actualidad

    **Fuente:** Estaciones meteorológicas DMC

    **Nota:** La radiación UVB es importante para evaluar la exposición solar y riesgos para la salud.
    """
    data = db.query(VHumedadRadiacionUV).order_by(VHumedadRadiacionUV.mes).all()
    return data

# ============================
# ENDPOINTS - MP2.5 (Material Particulado Fino)
# ============================

@mp25_router.get(
    "/anual",
    response_model=List[Mp25AnualSchema],
    summary="Concentraciones anuales de MP2.5",
    description="Estadísticas anuales de Material Particulado fino (MP2.5) por estación de monitoreo."
)
async def get_mp25_anual(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas anuales de concentraciones de MP2.5.

    **MP2.5:** Partículas en suspensión con diámetro ≤ 2.5 micrones. Son las más peligrosas
    para la salud ya que pueden penetrar profundamente en los pulmones y el torrente sanguíneo.

    **Datos incluidos:**
    - Concentración máxima horaria anual (µg/m³)
    - Concentración mínima horaria anual (µg/m³)
    - Percentiles 50, 90, 95 y 98 de concentraciones

    **Periodo:** Datos desde 2000 hasta la actualidad

    **Norma Chilena:** La norma primaria de calidad del aire establece 50 µg/m³ como promedio anual.

    **Fuente:** Red de Monitoreo de Calidad del Aire SINCA (Sistema de Información Nacional de Calidad del Aire)
    """
    data = db.query(VMp25Anual).order_by(VMp25Anual.anio).all()
    return data

@mp25_router.get(
    "/mensual",
    response_model=List[Mp25MensualSchema],
    summary="Concentraciones mensuales de MP2.5",
    description="Promedios mensuales de Material Particulado fino (MP2.5) por estación."
)
async def get_mp25_mensual(db: Session = Depends(get_db)):
    """
    Obtiene promedios mensuales de concentraciones de MP2.5.

    **Datos incluidos:**
    - Promedio mensual de concentración (µg/m³)

    **Periodo:** Datos desde 2000 hasta la actualidad

    **Uso:** Útil para identificar patrones estacionales y tendencias temporales de contaminación atmosférica.

    **Fuente:** Red SINCA
    """
    data = db.query(VMp25Mensual).order_by(VMp25Mensual.mes).all()
    return data

# ============================
# ENDPOINTS - MP10 (Material Particulado Respirable)
# ============================

@mp10_router.get(
    "/anual",
    response_model=List[Mp10AnualSchema],
    summary="Concentraciones anuales de MP10",
    description="Estadísticas anuales de Material Particulado respirable (MP10) por estación de monitoreo."
)
async def get_mp10_anual(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas anuales de concentraciones de MP10.

    **MP10:** Partículas en suspensión con diámetro ≤ 10 micrones. Incluye polvo, polen,
    cenizas y partículas de combustión.

    **Datos incluidos:**
    - Concentración máxima horaria anual (µg/m³)
    - Concentración mínima horaria anual (µg/m³)
    - Percentiles 50, 90, 95 y 98 de concentraciones

    **Periodo:** Datos desde 2000 hasta la actualidad

    **Norma Chilena:** 150 µg/m³ promedio de 24 horas (no más de 1 vez al año)

    **Fuente:** Red SINCA
    """
    data = db.query(VMp10Anual).order_by(VMp10Anual.anio).all()
    return data

@mp10_router.get(
    "/mensual",
    response_model=List[Mp10MensualSchema],
    summary="Concentraciones mensuales de MP10",
    description="Promedios mensuales de Material Particulado respirable (MP10) por estación."
)
async def get_mp10_mensual(db: Session = Depends(get_db)):
    """
    Obtiene promedios mensuales de concentraciones de MP10.

    **Datos incluidos:**
    - Promedio mensual de concentración (µg/m³)

    **Periodo:** Datos desde 2000 hasta la actualidad

    **Fuente:** Red SINCA
    """
    data = db.query(VMp10Mensual).order_by(VMp10Mensual.mes).all()
    return data

# ============================
# ENDPOINTS - O3 (Ozono Troposférico)
# ============================

@o3_router.get(
    "/anual",
    response_model=List[O3AnualSchema],
    summary="Concentraciones anuales de Ozono",
    description="Estadísticas anuales de Ozono troposférico (O3) por estación de monitoreo."
)
async def get_o3_anual(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas anuales de concentraciones de O3 troposférico.

    **O3 Troposférico:** Contaminante secundario formado por reacciones fotoquímicas entre
    óxidos de nitrógeno y compuestos orgánicos volátiles en presencia de luz solar.

    **Datos incluidos:**
    - Concentración máxima horaria anual (ppb)
    - Concentración mínima horaria anual (ppb)
    - Percentiles 50, 90, 95, 98 y 99 de concentraciones

    **Periodo:** Datos desde 2000 hasta la actualidad

    **Efectos:** Irritación de vías respiratorias, daño pulmonar, problemas cardiovasculares.

    **Norma Chilena:** 61 ppb como promedio móvil de 8 horas

    **Fuente:** Red SINCA
    """
    data = db.query(VO3Anual).order_by(VO3Anual.anio).all()
    return data

@o3_router.get(
    "/mensual",
    response_model=List[O3MensualSchema],
    summary="Concentraciones mensuales de Ozono",
    description="Promedios mensuales de Ozono troposférico (O3) por estación."
)
async def get_o3_mensual(db: Session = Depends(get_db)):
    """
    Obtiene promedios mensuales de concentraciones de O3.

    **Datos incluidos:**
    - Promedio mensual de concentración (ppb)

    **Periodo:** Datos desde 2000 hasta la actualidad

    **Nota:** Las concentraciones de ozono suelen ser mayores en verano debido a mayor radiación solar.

    **Fuente:** Red SINCA
    """
    data = db.query(VO3Mensual).order_by(VO3Mensual.mes).all()
    return data

# ============================
# ENDPOINTS - SO2 (Dióxido de Azufre)
# ============================

@so2_router.get(
    "/anual",
    response_model=List[So2AnualSchema],
    summary="Concentraciones anuales de SO2",
    description="Estadísticas anuales de Dióxido de Azufre (SO2) por estación de monitoreo."
)
async def get_so2_anual(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas anuales de concentraciones de SO2.

    **SO2:** Gas incoloro con olor penetrante, producido principalmente por la quema de
    combustibles fósiles que contienen azufre y procesos industriales.

    **Datos incluidos:**
    - Concentración máxima horaria anual (ppb)
    - Concentración mínima horaria anual (ppb)
    - Percentiles 50, 90, 95, 98 y 99 de concentraciones

    **Periodo:** Datos desde 2009 hasta la actualidad

    **Efectos:** Irritación del tracto respiratorio, agravamiento de enfermedades pulmonares.

    **Norma Chilena:** 250 µg/m³ (96 ppb) como promedio de 24 horas

    **Fuente:** Red SINCA
    """
    data = db.query(VSo2Anual).order_by(VSo2Anual.anio).all()
    return data

@so2_router.get(
    "/mensual",
    response_model=List[So2MensualSchema],
    summary="Concentraciones mensuales de SO2",
    description="Promedios mensuales de Dióxido de Azufre (SO2) por estación."
)
async def get_so2_mensual(db: Session = Depends(get_db)):
    """
    Obtiene promedios mensuales de concentraciones de SO2.

    **Datos incluidos:**
    - Promedio mensual de concentración (ppb)

    **Periodo:** Datos desde 2009 hasta la actualidad

    **Fuente:** Red SINCA
    """
    data = db.query(VSo2Mensual).order_by(VSo2Mensual.mes).all()
    return data

# ============================
# ENDPOINTS - NO2 (Dióxido de Nitrógeno)
# ============================

@no2_router.get(
    "/anual",
    response_model=List[No2AnualSchema],
    summary="Concentraciones anuales de NO2",
    description="Estadísticas anuales de Dióxido de Nitrógeno (NO2) por estación de monitoreo."
)
async def get_no2_anual(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas anuales de concentraciones de NO2.

    **NO2:** Gas rojizo-marrón con olor acre, producido principalmente por vehículos motorizados
    y procesos de combustión a alta temperatura.

    **Datos incluidos:**
    - Concentración máxima horaria anual (ppb)
    - Concentración mínima horaria anual (ppb)
    - Percentiles 50, 90, 95, 98 y 99 de concentraciones

    **Periodo:** Datos desde 2009 hasta la actualidad

    **Efectos:** Inflamación de vías respiratorias, disminución de función pulmonar,
    aumento de susceptibilidad a infecciones respiratorias.

    **Norma Chilena:** 100 ppb como promedio anual

    **Fuente:** Red SINCA
    """
    data = db.query(VNo2Anual).order_by(VNo2Anual.anio).all()
    return data

@no2_router.get(
    "/mensual",
    response_model=List[No2MensualSchema],
    summary="Concentraciones mensuales de NO2",
    description="Promedios mensuales de Dióxido de Nitrógeno (NO2) por estación."
)
async def get_no2_mensual(db: Session = Depends(get_db)):
    """
    Obtiene promedios mensuales de concentraciones de NO2.

    **Datos incluidos:**
    - Promedio mensual de concentración (ppb)

    **Periodo:** Datos desde 2009 hasta la actualidad

    **Fuente:** Red SINCA
    """
    data = db.query(VNo2Mensual).order_by(VNo2Mensual.mes).all()
    return data

# ============================
# ENDPOINTS - CO (Monóxido de Carbono)
# ============================

@co_router.get(
    "/anual",
    response_model=List[CoAnualSchema],
    summary="Concentraciones anuales de CO",
    description="Estadísticas anuales de Monóxido de Carbono (CO) por estación de monitoreo."
)
async def get_co_anual(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas anuales de concentraciones de CO.

    **CO:** Gas incoloro e inodoro producido por combustión incompleta de combustibles fósiles.
    Principal fuente: emisiones vehiculares.

    **Datos incluidos:**
    - Concentración máxima horaria anual (ppm)
    - Concentración mínima horaria anual (ppm)
    - Percentiles 50, 90, 95, 98 y 99 de concentraciones

    **Periodo:** Datos desde 2000 hasta la actualidad

    **Efectos:** Reduce capacidad de transporte de oxígeno en sangre, afecta sistema cardiovascular
    y nervioso, puede ser letal en altas concentraciones.

    **Norma Chilena:** 9 ppm como promedio móvil de 8 horas

    **Fuente:** Red SINCA
    """
    data = db.query(VCoAnual).order_by(VCoAnual.anio).all()
    return data

@co_router.get(
    "/mensual",
    response_model=List[CoMensualSchema],
    summary="Concentraciones mensuales de CO",
    description="Promedios mensuales de Monóxido de Carbono (CO) por estación."
)
async def get_co_mensual(db: Session = Depends(get_db)):
    """
    Obtiene promedios mensuales de concentraciones de CO.

    **Datos incluidos:**
    - Promedio mensual de concentración (ppm)

    **Periodo:** Datos desde 2000 hasta la actualidad

    **Fuente:** Red SINCA
    """
    data = db.query(VCoMensual).order_by(VCoMensual.mes).all()
    return data

# ============================
# ENDPOINTS - NO (Óxido de Nitrógeno)
# ============================

@no_router.get(
    "/anual",
    response_model=List[NoAnualSchema],
    summary="Concentraciones anuales de NO",
    description="Estadísticas anuales de Óxido de Nitrógeno (NO) por estación de monitoreo."
)
async def get_no_anual(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas anuales de concentraciones de NO.

    **NO:** Gas incoloro producido por procesos de combustión a alta temperatura.
    Se oxida rápidamente a NO2 en la atmósfera.

    **Datos incluidos:**
    - Concentración máxima horaria anual (ppb)
    - Concentración mínima horaria anual (ppb)
    - Percentiles 50, 90, 95, 98 y 99 de concentraciones

    **Periodo:** Datos desde 2009 hasta la actualidad

    **Fuente:** Red SINCA
    """
    data = db.query(VNoAnual).order_by(VNoAnual.anio).all()
    return data

@no_router.get(
    "/mensual",
    response_model=List[NoMensualSchema],
    summary="Concentraciones mensuales de NO",
    description="Promedios mensuales de Óxido de Nitrógeno (NO) por estación."
)
async def get_no_mensual(db: Session = Depends(get_db)):
    """
    Obtiene promedios mensuales de concentraciones de NO.

    **Datos incluidos:**
    - Promedio mensual de concentración (ppb)

    **Periodo:** Datos desde 2009 hasta la actualidad

    **Fuente:** Red SINCA
    """
    data = db.query(VNoMensual).order_by(VNoMensual.mes).all()
    return data

# ============================
# ENDPOINTS - NOx (Óxidos de Nitrógeno)
# ============================

@nox_router.get(
    "/anual",
    response_model=List[NoxAnualSchema],
    summary="Concentraciones anuales de NOx",
    description="Estadísticas anuales de Óxidos de Nitrógeno (NOx = NO + NO2) por estación de monitoreo."
)
async def get_nox_anual(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas anuales de concentraciones de NOx.

    **NOx:** Suma de NO y NO2. Indicador importante de contaminación vehicular e industrial.

    **Datos incluidos:**
    - Concentración máxima horaria anual (ppb)
    - Concentración mínima horaria anual (ppb)
    - Percentiles 50, 90, 95, 98 y 99 de concentraciones

    **Periodo:** Datos desde 2009 hasta la actualidad

    **Importancia:** Los NOx son precursores del ozono troposférico y contribuyen a la lluvia ácida.

    **Fuente:** Red SINCA
    """
    data = db.query(VNoxAnual).order_by(VNoxAnual.anio).all()
    return data

@nox_router.get(
    "/mensual",
    response_model=List[NoxMensualSchema],
    summary="Concentraciones mensuales de NOx",
    description="Promedios mensuales de Óxidos de Nitrógeno (NOx) por estación."
)
async def get_nox_mensual(db: Session = Depends(get_db)):
    """
    Obtiene promedios mensuales de concentraciones de NOx.

    **Datos incluidos:**
    - Promedio mensual de concentración (ppb)

    **Periodo:** Datos desde 2009 hasta la actualidad

    **Fuente:** Red SINCA
    """
    data = db.query(VNoxMensual).order_by(VNoxMensual.mes).all()
    return data

# ============================
# ENDPOINTS - EVENTOS CLIMÁTICOS
# ============================

@eventos_router.get(
    "/olas-calor",
    response_model=List[OlasCalorSchema],
    summary="Eventos de olas de calor",
    description="Número de eventos de olas de calor registrados por región y año."
)
async def get_olas_calor(db: Session = Depends(get_db)):
    """
    Obtiene el número de eventos de olas de calor por región y año.

    **Ola de Calor:** Evento climático extremo caracterizado por temperaturas anormalmente
    altas durante un período prolongado (3 o más días consecutivos).

    **Datos incluidos:**
    - Año del evento
    - Región afectada
    - Número de eventos registrados

    **Periodo:** Datos desde 2010 hasta la actualidad

    **Importancia:** Las olas de calor tienen impactos significativos en salud pública,
    agricultura, recursos hídricos y ecosistemas. Su frecuencia e intensidad están aumentando
    debido al cambio climático.

    **Fuente:** DMC (Dirección Meteorológica de Chile)
    """
    data = db.query(VNumEventosDeOlasDeCalor).order_by(VNumEventosDeOlasDeCalor.mes).all()
    return data

# Incluir sub-routers en el router principal
router.include_router(general_router)
router.include_router(mp25_router)
router.include_router(mp10_router)
router.include_router(o3_router)
router.include_router(so2_router)
router.include_router(no2_router)
router.include_router(co_router)
router.include_router(no_router)
router.include_router(nox_router)
router.include_router(eventos_router)

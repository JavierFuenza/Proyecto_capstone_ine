from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.dependencies import get_db
from models.aire import (
    VTemperatura, VHumedadRadiacionUV, VNumEventosDeOlasDeCalor,
    VMp25Anual, VMp25Mensual, VMp10Anual, VMp10Mensual,
    VO3Anual, VO3Mensual, VSo2Anual, VSo2Mensual,
    VNo2Anual, VNo2Mensual, VCoAnual, VCoMensual
)
from schemas.metricas import (
    TemperaturaData, HumedadRadiacionUVData, OlasDeCalorData,
    ContaminanteAnualData, ContaminanteMensualData, MetricaResponse
)

router = APIRouter(
    prefix="/metricas",
    tags=["Métricas"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/tabs/{nombre_estacion}")
async def get_metricas_disponibles(nombre_estacion: str, db: Session = Depends(get_db)):
    """
    Obtener las métricas disponibles para una estación específica.
    Retorna un array de strings con las métricas que tienen datos.

    Posibles valores: 'temperatura', 'mp25', 'mp10', 'o3', 'so2', 'no2', 'co', 'otros'
    """
    metricas_disponibles = []

    # Verificar Temperatura
    temp_count = db.query(VTemperatura).filter(
        VTemperatura.estacion == nombre_estacion
    ).count()
    if temp_count > 0:
        metricas_disponibles.append('temperatura')

    # Verificar MP2.5
    mp25_count = db.query(VMp25Anual).filter(
        VMp25Anual.estacion == nombre_estacion
    ).count() + db.query(VMp25Mensual).filter(
        VMp25Mensual.estacion == nombre_estacion
    ).count()
    if mp25_count > 0:
        metricas_disponibles.append('mp25')

    # Verificar MP10
    mp10_count = db.query(VMp10Anual).filter(
        VMp10Anual.estacion == nombre_estacion
    ).count() + db.query(VMp10Mensual).filter(
        VMp10Mensual.estacion == nombre_estacion
    ).count()
    if mp10_count > 0:
        metricas_disponibles.append('mp10')

    # Verificar O3
    o3_count = db.query(VO3Anual).filter(
        VO3Anual.estacion == nombre_estacion
    ).count() + db.query(VO3Mensual).filter(
        VO3Mensual.estacion == nombre_estacion
    ).count()
    if o3_count > 0:
        metricas_disponibles.append('o3')

    # Verificar SO2
    so2_count = db.query(VSo2Anual).filter(
        VSo2Anual.estacion == nombre_estacion
    ).count() + db.query(VSo2Mensual).filter(
        VSo2Mensual.estacion == nombre_estacion
    ).count()
    if so2_count > 0:
        metricas_disponibles.append('so2')

    # Verificar NO2
    no2_count = db.query(VNo2Anual).filter(
        VNo2Anual.estacion == nombre_estacion
    ).count() + db.query(VNo2Mensual).filter(
        VNo2Mensual.estacion == nombre_estacion
    ).count()
    if no2_count > 0:
        metricas_disponibles.append('no2')

    # Verificar CO
    co_count = db.query(VCoAnual).filter(
        VCoAnual.estacion == nombre_estacion
    ).count() + db.query(VCoMensual).filter(
        VCoMensual.estacion == nombre_estacion
    ).count()
    if co_count > 0:
        metricas_disponibles.append('co')

    # Verificar Humedad, Radiación UV y Olas de Calor
    humedad_rad_uv_count = db.query(VHumedadRadiacionUV).filter(
        VHumedadRadiacionUV.estacion == nombre_estacion
    ).count() + db.query(VNumEventosDeOlasDeCalor).filter(
        VNumEventosDeOlasDeCalor.estacion == nombre_estacion
    ).count()
    if humedad_rad_uv_count > 0:
        metricas_disponibles.append('humedad_radiacion_uv')

    return {
        "estacion": nombre_estacion,
        "metricas_disponibles": metricas_disponibles
    }

@router.get("/temperatura/{nombre_estacion}", response_model=List[TemperaturaData])
async def get_temperatura(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de temperatura para una estación específica"""
    datos = db.query(VTemperatura).filter(
        VTemperatura.estacion == nombre_estacion
    ).order_by(VTemperatura.mes).all()

    if not datos:
        return []

    return datos

@router.get("/mp25/{nombre_estacion}")
async def get_mp25(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de MP2.5 (anuales y mensuales) para una estación"""
    anuales = db.query(VMp25Anual).filter(
        VMp25Anual.estacion == nombre_estacion
    ).order_by(VMp25Anual.anio).all()

    mensuales = db.query(VMp25Mensual).filter(
        VMp25Mensual.estacion == nombre_estacion
    ).order_by(VMp25Mensual.mes).all()

    # Convertir a formato común
    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.mp25_max_hor_anual,
        "min_hor_anual": d.mp25_min_hor_anual,
        "perc50": d.mp25_perc50,
        "perc90": d.mp25_perc90,
        "perc95": d.mp25_perc95,
        "perc98": float(d.mp25_perc98) if d.mp25_perc98 else None,
        "perc99": None
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": float(d.mp25_med_mens) if d.mp25_med_mens else None
    } for d in mensuales]

    return {
        "metrica": "mp25",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/mp10/{nombre_estacion}")
async def get_mp10(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de MP10 (anuales y mensuales) para una estación"""
    anuales = db.query(VMp10Anual).filter(
        VMp10Anual.estacion == nombre_estacion
    ).order_by(VMp10Anual.anio).all()

    mensuales = db.query(VMp10Mensual).filter(
        VMp10Mensual.estacion == nombre_estacion
    ).order_by(VMp10Mensual.mes).all()

    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.mp10_max_hor_anual,
        "min_hor_anual": d.mp10_min_hor_anual,
        "perc50": d.mp10_perc50,
        "perc90": d.mp10_perc90,
        "perc95": d.mp10_perc95,
        "perc98": float(d.mp10_perc98) if d.mp10_perc98 else None,
        "perc99": None
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": float(d.mp10_med_mens) if d.mp10_med_mens else None
    } for d in mensuales]

    return {
        "metrica": "mp10",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/o3/{nombre_estacion}")
async def get_o3(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de Ozono (anuales y mensuales) para una estación"""
    anuales = db.query(VO3Anual).filter(
        VO3Anual.estacion == nombre_estacion
    ).order_by(VO3Anual.anio).all()

    mensuales = db.query(VO3Mensual).filter(
        VO3Mensual.estacion == nombre_estacion
    ).order_by(VO3Mensual.mes).all()

    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.o3_max_hor_anual,
        "min_hor_anual": d.o3_min_hor_anual,
        "perc50": d.o3_perc50,
        "perc90": d.o3_perc90,
        "perc95": d.o3_perc95,
        "perc98": d.o3_perc98,
        "perc99": d.o3_perc99
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": d.o3_med_mens
    } for d in mensuales]

    return {
        "metrica": "o3",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/so2/{nombre_estacion}")
async def get_so2(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de SO2 (anuales y mensuales) para una estación"""
    anuales = db.query(VSo2Anual).filter(
        VSo2Anual.estacion == nombre_estacion
    ).order_by(VSo2Anual.anio).all()

    mensuales = db.query(VSo2Mensual).filter(
        VSo2Mensual.estacion == nombre_estacion
    ).order_by(VSo2Mensual.mes).all()

    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.so2_max_hor_anual,
        "min_hor_anual": d.so2_min_anual,
        "perc50": d.so2_perc50,
        "perc90": d.so2_perc90,
        "perc95": d.so2_perc95,
        "perc98": d.so2_perc98,
        "perc99": d.so2_perc99
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": d.so2_med_mens
    } for d in mensuales]

    return {
        "metrica": "so2",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/no2/{nombre_estacion}")
async def get_no2(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de NO2 (anuales y mensuales) para una estación"""
    anuales = db.query(VNo2Anual).filter(
        VNo2Anual.estacion == nombre_estacion
    ).order_by(VNo2Anual.anio).all()

    mensuales = db.query(VNo2Mensual).filter(
        VNo2Mensual.estacion == nombre_estacion
    ).order_by(VNo2Mensual.mes).all()

    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.no2_max_hor_anual,
        "min_hor_anual": d.no2_min_hor_anual,
        "perc50": d.no2_perc50,
        "perc90": d.no2_perc90,
        "perc95": d.no2_perc95,
        "perc98": d.no2_perc98,
        "perc99": d.no2_perc99
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": d.no2_med_mens
    } for d in mensuales]

    return {
        "metrica": "no2",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/co/{nombre_estacion}")
async def get_co(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de CO (anuales y mensuales) para una estación"""
    anuales = db.query(VCoAnual).filter(
        VCoAnual.estacion == nombre_estacion
    ).order_by(VCoAnual.anio).all()

    mensuales = db.query(VCoMensual).filter(
        VCoMensual.estacion == nombre_estacion
    ).order_by(VCoMensual.mes).all()

    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.co_max_hor_anual,
        "min_hor_anual": d.co_min_hor_anual,
        "perc50": d.co_perc50,
        "perc90": d.co_perc90,
        "perc95": d.co_perc95,
        "perc98": d.co_perc98,
        "perc99": d.co_perc99
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": d.co_med_mens
    } for d in mensuales]

    return {
        "metrica": "co",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/humedad_radiacion_uv/{nombre_estacion}")
async def get_humedad_radiacion_uv(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de Humedad, Radiación UV y Olas de Calor para una estación"""
    humedad_rad_uv = db.query(VHumedadRadiacionUV).filter(
        VHumedadRadiacionUV.estacion == nombre_estacion
    ).order_by(VHumedadRadiacionUV.mes).all()

    olas_calor = db.query(VNumEventosDeOlasDeCalor).filter(
        VNumEventosDeOlasDeCalor.estacion == nombre_estacion
    ).order_by(VNumEventosDeOlasDeCalor.mes).all()

    return {
        "estacion": nombre_estacion,
        "humedad_radiacion_uv": [
            {
                "mes": d.mes,
                "humedad_rel_med_mens": d.humedad_rel_med_mens,
                "rad_global_med": d.rad_global_med,
                "uvb_prom": d.uvb_prom
            } for d in humedad_rad_uv
        ],
        "olas_de_calor": [
            {
                "mes": d.mes,
                "num_eventos": d.num_eventos_de_olas_de_calor
            } for d in olas_calor
        ],
        "tiene_datos": len(humedad_rad_uv) > 0 or len(olas_calor) > 0
    }

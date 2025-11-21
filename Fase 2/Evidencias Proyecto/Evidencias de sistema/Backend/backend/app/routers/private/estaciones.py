from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from typing import List, Optional

from core.dependencies import get_db
from models.estaciones import Estacion
from models.aire import (
    VTemperatura, VHumedadRadiacionUV, VNumEventosDeOlasDeCalor,
    VMp25Anual, VMp25Mensual, VMp10Anual, VMp10Mensual,
    VO3Anual, VO3Mensual, VSo2Anual, VSo2Mensual,
    VNo2Anual, VNo2Mensual, VCoAnual, VCoMensual,
    VNoAnual, VNoMensual, VNoxAnual, VNoxMensual
)
from schemas.estaciones import EstacionSchema, RegionSchema, EstacionMetricasSchema, EstacionSubmetricasSchema, DatosSubmetricaSchema, EstacionConMetricasSchema

router = APIRouter(
    prefix="/estaciones",
    tags=["Estaciones"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/metricas", response_model=EstacionMetricasSchema)
async def get_estacion_metricas(
    db: Session = Depends(get_db),
    nombre: str = Query(..., description="Nombre de la estación")
):
    """Obtener métricas disponibles para una estación específica por nombre"""

    # Buscar la estación
    estacion = db.query(Estacion).filter(Estacion.nombre == nombre).first()
    if not estacion:
        raise HTTPException(
            status_code=404,
            detail=f"Estación '{nombre}' no encontrada"
        )

    # Verificar qué métricas tiene disponibles
    metricas = []

    # Verificar Temperatura
    tiene_temperatura = db.query(VTemperatura).filter(
        VTemperatura.estacion == estacion.nombre
    ).first() is not None
    if tiene_temperatura:
        metricas.append("Temperatura")

    # Verificar Humedad, Radiación y UV
    tiene_humedad_radiacion_uv = db.query(VHumedadRadiacionUV).filter(
        VHumedadRadiacionUV.estacion == estacion.nombre
    ).first() is not None
    if tiene_humedad_radiacion_uv:
        metricas.append("Humedad Radiación y UV")

    # Verificar Contaminantes (MP2.5, MP10, O3, SO2, NO2, CO, NO, NOX)
    tiene_contaminantes = any([
        db.query(VMp25Anual).filter(VMp25Anual.estacion == estacion.nombre).first() is not None,
        db.query(VMp25Mensual).filter(VMp25Mensual.estacion == estacion.nombre).first() is not None,
        db.query(VMp10Anual).filter(VMp10Anual.estacion == estacion.nombre).first() is not None,
        db.query(VMp10Mensual).filter(VMp10Mensual.estacion == estacion.nombre).first() is not None,
        db.query(VO3Anual).filter(VO3Anual.estacion == estacion.nombre).first() is not None,
        db.query(VO3Mensual).filter(VO3Mensual.estacion == estacion.nombre).first() is not None,
        db.query(VSo2Anual).filter(VSo2Anual.estacion == estacion.nombre).first() is not None,
        db.query(VSo2Mensual).filter(VSo2Mensual.estacion == estacion.nombre).first() is not None,
        db.query(VNo2Anual).filter(VNo2Anual.estacion == estacion.nombre).first() is not None,
        db.query(VNo2Mensual).filter(VNo2Mensual.estacion == estacion.nombre).first() is not None,
        db.query(VCoAnual).filter(VCoAnual.estacion == estacion.nombre).first() is not None,
        db.query(VCoMensual).filter(VCoMensual.estacion == estacion.nombre).first() is not None,
        db.query(VNoAnual).filter(VNoAnual.estacion == estacion.nombre).first() is not None,
        db.query(VNoMensual).filter(VNoMensual.estacion == estacion.nombre).first() is not None,
        db.query(VNoxAnual).filter(VNoxAnual.estacion == estacion.nombre).first() is not None,
        db.query(VNoxMensual).filter(VNoxMensual.estacion == estacion.nombre).first() is not None,
    ])
    if tiene_contaminantes:
        metricas.append("Contaminantes")

    # Verificar Eventos de Olas de Calor
    tiene_olas_calor = db.query(VNumEventosDeOlasDeCalor).filter(
        VNumEventosDeOlasDeCalor.estacion == estacion.nombre
    ).first() is not None
    if tiene_olas_calor:
        metricas.append("Eventos de Olas de Calor")

    return {
        "nombre": estacion.nombre,
        "descripcion": estacion.descripcion,
        "metricas_disponibles": metricas
    }

@router.get("/con-metricas", response_model=List[EstacionConMetricasSchema])
async def get_all_estaciones_con_metricas(
    db: Session = Depends(get_db),
    numero_region: Optional[int] = Query(None, description="Filtrar por número de región")
):
    """Obtener todas las estaciones con información de qué métricas tiene cada una"""
    from sqlalchemy import exists

    # Obtener todas las estaciones
    query = db.query(Estacion)
    if numero_region is not None:
        query = query.filter(Estacion.numero_region == numero_region)

    estaciones = query.order_by(Estacion.nombre).all()

    # Pre-cargar qué estaciones tienen qué métricas usando sets (más eficiente)
    estaciones_con_temperatura = set(
        row[0] for row in db.query(distinct(VTemperatura.estacion)).all()
    )

    estaciones_con_humedad = set(
        row[0] for row in db.query(distinct(VHumedadRadiacionUV.estacion)).all()
    )

    estaciones_con_olas_calor = set(
        row[0] for row in db.query(distinct(VNumEventosDeOlasDeCalor.estacion)).all()
    )

    # Para contaminantes específicos, cargar por tipo
    estaciones_con_mp25 = set()
    for tabla in [VMp25Anual, VMp25Mensual]:
        estaciones_con_mp25.update(row[0] for row in db.query(distinct(tabla.estacion)).all())

    estaciones_con_mp10 = set()
    for tabla in [VMp10Anual, VMp10Mensual]:
        estaciones_con_mp10.update(row[0] for row in db.query(distinct(tabla.estacion)).all())

    estaciones_con_o3 = set()
    for tabla in [VO3Anual, VO3Mensual]:
        estaciones_con_o3.update(row[0] for row in db.query(distinct(tabla.estacion)).all())

    estaciones_con_so2 = set()
    for tabla in [VSo2Anual, VSo2Mensual]:
        estaciones_con_so2.update(row[0] for row in db.query(distinct(tabla.estacion)).all())

    estaciones_con_no2 = set()
    for tabla in [VNo2Anual, VNo2Mensual]:
        estaciones_con_no2.update(row[0] for row in db.query(distinct(tabla.estacion)).all())

    estaciones_con_co = set()
    for tabla in [VCoAnual, VCoMensual]:
        estaciones_con_co.update(row[0] for row in db.query(distinct(tabla.estacion)).all())

    result = []
    for estacion in estaciones:
        metricas = []
        contaminantes_list = []

        # Verificar temperatura
        tiene_temperatura = estacion.nombre in estaciones_con_temperatura
        if tiene_temperatura:
            metricas.append("Temperatura")

        # Verificar humedad
        tiene_humedad = estacion.nombre in estaciones_con_humedad
        if tiene_humedad:
            metricas.append("Humedad Radiación y UV")

        # Verificar cada contaminante específico
        if estacion.nombre in estaciones_con_mp25:
            contaminantes_list.append("mp25")
        if estacion.nombre in estaciones_con_mp10:
            contaminantes_list.append("mp10")
        if estacion.nombre in estaciones_con_o3:
            contaminantes_list.append("o3")
        if estacion.nombre in estaciones_con_so2:
            contaminantes_list.append("so2")
        if estacion.nombre in estaciones_con_no2:
            contaminantes_list.append("no2")
        if estacion.nombre in estaciones_con_co:
            contaminantes_list.append("co")

        if contaminantes_list:
            metricas.append("Contaminantes")

        # Verificar olas de calor
        if estacion.nombre in estaciones_con_olas_calor:
            metricas.append("Eventos de Olas de Calor")

        result.append({
            "nombre": estacion.nombre,
            "latitud": estacion.latitud,
            "longitud": estacion.longitud,
            "numero_region": estacion.numero_region,
            "nombre_region": estacion.nombre_region,
            "descripcion": estacion.descripcion,
            "metricas_disponibles": metricas,
            "metricas_detalladas": {
                "temperatura": tiene_temperatura,
                "humedad_radiacion_uv": tiene_humedad,
                "contaminantes": contaminantes_list
            }
        })

    return result

@router.get("/submetricas", response_model=EstacionSubmetricasSchema)
async def get_estacion_submetricas(
    db: Session = Depends(get_db),
    metrica: str = Query(..., description="Categoría de métrica: Temperatura, Humedad Radiación y UV, Contaminantes, Eventos de Olas de Calor"),
    nombre: str = Query(..., description="Nombre de la estación")
):
    """Obtener submmétricas específicas disponibles (columnas con >= 2 registros no nulos)"""

    # Buscar la estación
    estacion = db.query(Estacion).filter(Estacion.nombre == nombre).first()
    if not estacion:
        raise HTTPException(
            status_code=404,
            detail=f"Estación '{nombre}' no encontrada"
        )

    submetricas = []

    # ====================
    # TEMPERATURA
    # ====================
    if metrica.lower() == "temperatura":
        # Verificar cada columna de la vista v_temperatura
        if db.query(VTemperatura).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_max_absoluta.isnot(None)
        ).count() >= 2:
            submetricas.append("Temperatura Máxima Absoluta")

        if db.query(VTemperatura).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_min_absoluta.isnot(None)
        ).count() >= 2:
            submetricas.append("Temperatura Mínima Absoluta")

        if db.query(VTemperatura).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_max_med.isnot(None)
        ).count() >= 2:
            submetricas.append("Temperatura Máxima Media")

        if db.query(VTemperatura).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_min_med.isnot(None)
        ).count() >= 2:
            submetricas.append("Temperatura Mínima Media")

        if db.query(VTemperatura).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_med.isnot(None)
        ).count() >= 2:
            submetricas.append("Temperatura Media")

    # ====================
    # HUMEDAD, RADIACIÓN Y UV
    # ====================
    elif "humedad" in metrica.lower() or "radiación" in metrica.lower() or "radiacion" in metrica.lower():
        # Verificar cada columna de la vista v_humedad_radiacion_uv
        if db.query(VHumedadRadiacionUV).filter(
            VHumedadRadiacionUV.estacion == estacion.nombre,
            VHumedadRadiacionUV.humedad_rel_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("Humedad Relativa Media Mensual")

        if db.query(VHumedadRadiacionUV).filter(
            VHumedadRadiacionUV.estacion == estacion.nombre,
            VHumedadRadiacionUV.rad_global_med.isnot(None)
        ).count() >= 2:
            submetricas.append("Radiación Global Media")

        if db.query(VHumedadRadiacionUV).filter(
            VHumedadRadiacionUV.estacion == estacion.nombre,
            VHumedadRadiacionUV.uvb_prom.isnot(None)
        ).count() >= 2:
            submetricas.append("UVB Promedio")

    # ====================
    # CONTAMINANTES
    # ====================
    elif metrica.lower() == "contaminantes":
        # MP2.5 Anual - Verificar cada columna
        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Máximo Horario Anual")

        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Mínimo Horario Anual")

        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Percentil 50")

        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Percentil 90")

        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Percentil 95")

        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Percentil 98")

        # MP2.5 Mensual
        if db.query(VMp25Mensual).filter(
            VMp25Mensual.estacion == estacion.nombre,
            VMp25Mensual.mp25_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Media Mensual")

        # MP10 Anual - Verificar cada columna
        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Máximo Horario Anual")

        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Mínimo Horario Anual")

        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Percentil 50")

        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Percentil 90")

        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Percentil 95")

        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Percentil 98")

        # MP10 Mensual
        if db.query(VMp10Mensual).filter(
            VMp10Mensual.estacion == estacion.nombre,
            VMp10Mensual.mp10_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Media Mensual")

        # O3 Anual
        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Máximo Horario Anual")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Mínimo Horario Anual")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Percentil 50")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Percentil 90")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Percentil 95")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Percentil 98")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Percentil 99")

        # O3 Mensual
        if db.query(VO3Mensual).filter(
            VO3Mensual.estacion == estacion.nombre,
            VO3Mensual.o3_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Media Mensual")

        # SO2 Anual
        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Máximo Horario Anual")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_min_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Mínimo Anual")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Percentil 50")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Percentil 90")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Percentil 95")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Percentil 98")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Percentil 99")

        # SO2 Mensual
        if db.query(VSo2Mensual).filter(
            VSo2Mensual.estacion == estacion.nombre,
            VSo2Mensual.so2_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Media Mensual")

        # NO2 Anual
        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Máximo Horario Anual")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Mínimo Horario Anual")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Percentil 50")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Percentil 90")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Percentil 95")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Percentil 98")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Percentil 99")

        # NO2 Mensual
        if db.query(VNo2Mensual).filter(
            VNo2Mensual.estacion == estacion.nombre,
            VNo2Mensual.no2_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Media Mensual")

        # CO Anual
        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Máximo Horario Anual")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Mínimo Horario Anual")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Percentil 50")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Percentil 90")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Percentil 95")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Percentil 98")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Percentil 99")

        # CO Mensual
        if db.query(VCoMensual).filter(
            VCoMensual.estacion == estacion.nombre,
            VCoMensual.co_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Media Mensual")

        # NO Anual
        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Máximo Horario Anual")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Mínimo Horario Anual")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Percentil 50")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Percentil 90")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Percentil 95")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Percentil 98")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Percentil 99")

        # NO Mensual
        if db.query(VNoMensual).filter(
            VNoMensual.estacion == estacion.nombre,
            VNoMensual.no_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Media Mensual")

        # NOX Anual
        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Máximo Horario Anual")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Mínimo Horario Anual")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Percentil 50")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Percentil 90")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Percentil 95")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Percentil 98")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Percentil 99")

        # NOX Mensual
        if db.query(VNoxMensual).filter(
            VNoxMensual.estacion == estacion.nombre,
            VNoxMensual.nox_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Media Mensual")

    # ====================
    # EVENTOS DE OLAS DE CALOR
    # ====================
    elif "olas de calor" in metrica.lower() or "eventos" in metrica.lower():
        if db.query(VNumEventosDeOlasDeCalor).filter(
            VNumEventosDeOlasDeCalor.estacion == estacion.nombre,
            VNumEventosDeOlasDeCalor.num_eventos_de_olas_de_calor.isnot(None)
        ).count() >= 2:
            submetricas.append("Número de Eventos de Olas de Calor")

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Métrica '{metrica}' no válida. Use: Temperatura, Humedad Radiación y UV, Contaminantes, o Eventos de Olas de Calor"
        )

    return {
        "nombre": estacion.nombre,
        "metrica": metrica,
        "submetricas_disponibles": submetricas
    }

@router.get("/datos-submetrica", response_model=DatosSubmetricaSchema)
async def get_datos_submetrica(
    db: Session = Depends(get_db),
    submetrica: str = Query(..., description="Nombre exacto de la submétrica"),
    nombre: str = Query(..., description="Nombre de la estación")
):
    """Obtener datos históricos de una submétrica específica para graficar"""

    # Buscar la estación
    estacion = db.query(Estacion).filter(Estacion.nombre == nombre).first()
    if not estacion:
        raise HTTPException(
            status_code=404,
            detail=f"Estación '{nombre}' no encontrada"
        )

    datos = []

    # ====================
    # TEMPERATURA
    # ====================
    if submetrica == "Temperatura Máxima Absoluta":
        registros = db.query(VTemperatura.mes, VTemperatura.temp_max_absoluta).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_max_absoluta.isnot(None)
        ).order_by(VTemperatura.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.temp_max_absoluta)} for r in registros]

    elif submetrica == "Temperatura Mínima Absoluta":
        registros = db.query(VTemperatura.mes, VTemperatura.temp_min_absoluta).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_min_absoluta.isnot(None)
        ).order_by(VTemperatura.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.temp_min_absoluta)} for r in registros]

    elif submetrica == "Temperatura Máxima Media":
        registros = db.query(VTemperatura.mes, VTemperatura.temp_max_med).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_max_med.isnot(None)
        ).order_by(VTemperatura.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.temp_max_med)} for r in registros]

    elif submetrica == "Temperatura Mínima Media":
        registros = db.query(VTemperatura.mes, VTemperatura.temp_min_med).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_min_med.isnot(None)
        ).order_by(VTemperatura.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.temp_min_med)} for r in registros]

    elif submetrica == "Temperatura Media":
        registros = db.query(VTemperatura.mes, VTemperatura.temp_med).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_med.isnot(None)
        ).order_by(VTemperatura.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.temp_med)} for r in registros]

    # ====================
    # HUMEDAD, RADIACIÓN Y UV
    # ====================
    elif submetrica == "Humedad Relativa Media Mensual":
        registros = db.query(VHumedadRadiacionUV.mes, VHumedadRadiacionUV.humedad_rel_med_mens).filter(
            VHumedadRadiacionUV.estacion == estacion.nombre,
            VHumedadRadiacionUV.humedad_rel_med_mens.isnot(None)
        ).order_by(VHumedadRadiacionUV.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.humedad_rel_med_mens)} for r in registros]

    elif submetrica == "Radiación Global Media":
        registros = db.query(VHumedadRadiacionUV.mes, VHumedadRadiacionUV.rad_global_med).filter(
            VHumedadRadiacionUV.estacion == estacion.nombre,
            VHumedadRadiacionUV.rad_global_med.isnot(None)
        ).order_by(VHumedadRadiacionUV.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.rad_global_med)} for r in registros]

    elif submetrica == "UVB Promedio":
        registros = db.query(VHumedadRadiacionUV.mes, VHumedadRadiacionUV.uvb_prom).filter(
            VHumedadRadiacionUV.estacion == estacion.nombre,
            VHumedadRadiacionUV.uvb_prom.isnot(None)
        ).order_by(VHumedadRadiacionUV.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.uvb_prom)} for r in registros]

    # ====================
    # CONTAMINANTES - MP2.5
    # ====================
    elif submetrica == "MP2.5 - Máximo Horario Anual":
        registros = db.query(VMp25Anual.anio, VMp25Anual.mp25_max_hor_anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_max_hor_anual.isnot(None)
        ).order_by(VMp25Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp25_max_hor_anual)} for r in registros]

    elif submetrica == "MP2.5 - Mínimo Horario Anual":
        registros = db.query(VMp25Anual.anio, VMp25Anual.mp25_min_hor_anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_min_hor_anual.isnot(None)
        ).order_by(VMp25Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp25_min_hor_anual)} for r in registros]

    elif submetrica == "MP2.5 - Percentil 50":
        registros = db.query(VMp25Anual.anio, VMp25Anual.mp25_perc50).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc50.isnot(None)
        ).order_by(VMp25Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp25_perc50)} for r in registros]

    elif submetrica == "MP2.5 - Percentil 90":
        registros = db.query(VMp25Anual.anio, VMp25Anual.mp25_perc90).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc90.isnot(None)
        ).order_by(VMp25Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp25_perc90)} for r in registros]

    elif submetrica == "MP2.5 - Percentil 95":
        registros = db.query(VMp25Anual.anio, VMp25Anual.mp25_perc95).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc95.isnot(None)
        ).order_by(VMp25Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp25_perc95)} for r in registros]

    elif submetrica == "MP2.5 - Percentil 98":
        registros = db.query(VMp25Anual.anio, VMp25Anual.mp25_perc98).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc98.isnot(None)
        ).order_by(VMp25Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp25_perc98)} for r in registros]

    elif submetrica == "MP2.5 - Media Mensual":
        registros = db.query(VMp25Mensual.mes, VMp25Mensual.mp25_med_mens).filter(
            VMp25Mensual.estacion == estacion.nombre,
            VMp25Mensual.mp25_med_mens.isnot(None)
        ).order_by(VMp25Mensual.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.mp25_med_mens)} for r in registros]

    # ====================
    # CONTAMINANTES - MP10
    # ====================
    elif submetrica == "MP10 - Máximo Horario Anual":
        registros = db.query(VMp10Anual.anio, VMp10Anual.mp10_max_hor_anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_max_hor_anual.isnot(None)
        ).order_by(VMp10Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp10_max_hor_anual)} for r in registros]

    elif submetrica == "MP10 - Mínimo Horario Anual":
        registros = db.query(VMp10Anual.anio, VMp10Anual.mp10_min_hor_anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_min_hor_anual.isnot(None)
        ).order_by(VMp10Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp10_min_hor_anual)} for r in registros]

    elif submetrica == "MP10 - Percentil 50":
        registros = db.query(VMp10Anual.anio, VMp10Anual.mp10_perc50).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc50.isnot(None)
        ).order_by(VMp10Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp10_perc50)} for r in registros]

    elif submetrica == "MP10 - Percentil 90":
        registros = db.query(VMp10Anual.anio, VMp10Anual.mp10_perc90).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc90.isnot(None)
        ).order_by(VMp10Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp10_perc90)} for r in registros]

    elif submetrica == "MP10 - Percentil 95":
        registros = db.query(VMp10Anual.anio, VMp10Anual.mp10_perc95).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc95.isnot(None)
        ).order_by(VMp10Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp10_perc95)} for r in registros]

    elif submetrica == "MP10 - Percentil 98":
        registros = db.query(VMp10Anual.anio, VMp10Anual.mp10_perc98).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc98.isnot(None)
        ).order_by(VMp10Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.mp10_perc98)} for r in registros]

    elif submetrica == "MP10 - Media Mensual":
        registros = db.query(VMp10Mensual.mes, VMp10Mensual.mp10_med_mens).filter(
            VMp10Mensual.estacion == estacion.nombre,
            VMp10Mensual.mp10_med_mens.isnot(None)
        ).order_by(VMp10Mensual.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.mp10_med_mens)} for r in registros]

    # ====================
    # CONTAMINANTES - O3 (OZONO)
    # ====================
    elif submetrica == "O3 - Máximo Horario Anual":
        registros = db.query(VO3Anual.anio, VO3Anual.o3_max_hor_anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_max_hor_anual.isnot(None)
        ).order_by(VO3Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.o3_max_hor_anual)} for r in registros]

    elif submetrica == "O3 - Mínimo Horario Anual":
        registros = db.query(VO3Anual.anio, VO3Anual.o3_min_hor_anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_min_hor_anual.isnot(None)
        ).order_by(VO3Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.o3_min_hor_anual)} for r in registros]

    elif submetrica == "O3 - Percentil 50":
        registros = db.query(VO3Anual.anio, VO3Anual.o3_perc50).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc50.isnot(None)
        ).order_by(VO3Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.o3_perc50)} for r in registros]

    elif submetrica == "O3 - Percentil 90":
        registros = db.query(VO3Anual.anio, VO3Anual.o3_perc90).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc90.isnot(None)
        ).order_by(VO3Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.o3_perc90)} for r in registros]

    elif submetrica == "O3 - Percentil 95":
        registros = db.query(VO3Anual.anio, VO3Anual.o3_perc95).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc95.isnot(None)
        ).order_by(VO3Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.o3_perc95)} for r in registros]

    elif submetrica == "O3 - Percentil 98":
        registros = db.query(VO3Anual.anio, VO3Anual.o3_perc98).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc98.isnot(None)
        ).order_by(VO3Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.o3_perc98)} for r in registros]

    elif submetrica == "O3 - Percentil 99":
        registros = db.query(VO3Anual.anio, VO3Anual.o3_perc99).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc99.isnot(None)
        ).order_by(VO3Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.o3_perc99)} for r in registros]

    elif submetrica == "O3 - Media Mensual":
        registros = db.query(VO3Mensual.mes, VO3Mensual.o3_med_mens).filter(
            VO3Mensual.estacion == estacion.nombre,
            VO3Mensual.o3_med_mens.isnot(None)
        ).order_by(VO3Mensual.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.o3_med_mens)} for r in registros]

    # ====================
    # CONTAMINANTES - SO2 (DIÓXIDO DE AZUFRE)
    # ====================
    elif submetrica == "SO2 - Máximo Horario Anual":
        registros = db.query(VSo2Anual.anio, VSo2Anual.so2_max_hor_anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_max_hor_anual.isnot(None)
        ).order_by(VSo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.so2_max_hor_anual)} for r in registros]

    elif submetrica == "SO2 - Mínimo Anual":
        registros = db.query(VSo2Anual.anio, VSo2Anual.so2_min_anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_min_anual.isnot(None)
        ).order_by(VSo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.so2_min_anual)} for r in registros]

    elif submetrica == "SO2 - Percentil 50":
        registros = db.query(VSo2Anual.anio, VSo2Anual.so2_perc50).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc50.isnot(None)
        ).order_by(VSo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.so2_perc50)} for r in registros]

    elif submetrica == "SO2 - Percentil 90":
        registros = db.query(VSo2Anual.anio, VSo2Anual.so2_perc90).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc90.isnot(None)
        ).order_by(VSo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.so2_perc90)} for r in registros]

    elif submetrica == "SO2 - Percentil 95":
        registros = db.query(VSo2Anual.anio, VSo2Anual.so2_perc95).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc95.isnot(None)
        ).order_by(VSo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.so2_perc95)} for r in registros]

    elif submetrica == "SO2 - Percentil 98":
        registros = db.query(VSo2Anual.anio, VSo2Anual.so2_perc98).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc98.isnot(None)
        ).order_by(VSo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.so2_perc98)} for r in registros]

    elif submetrica == "SO2 - Percentil 99":
        registros = db.query(VSo2Anual.anio, VSo2Anual.so2_perc99).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc99.isnot(None)
        ).order_by(VSo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.so2_perc99)} for r in registros]

    elif submetrica == "SO2 - Media Mensual":
        registros = db.query(VSo2Mensual.mes, VSo2Mensual.so2_med_mens).filter(
            VSo2Mensual.estacion == estacion.nombre,
            VSo2Mensual.so2_med_mens.isnot(None)
        ).order_by(VSo2Mensual.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.so2_med_mens)} for r in registros]

    # ====================
    # CONTAMINANTES - NO2 (DIÓXIDO DE NITRÓGENO)
    # ====================
    elif submetrica == "NO2 - Máximo Horario Anual":
        registros = db.query(VNo2Anual.anio, VNo2Anual.no2_max_hor_anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_max_hor_anual.isnot(None)
        ).order_by(VNo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no2_max_hor_anual)} for r in registros]

    elif submetrica == "NO2 - Mínimo Horario Anual":
        registros = db.query(VNo2Anual.anio, VNo2Anual.no2_min_hor_anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_min_hor_anual.isnot(None)
        ).order_by(VNo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no2_min_hor_anual)} for r in registros]

    elif submetrica == "NO2 - Percentil 50":
        registros = db.query(VNo2Anual.anio, VNo2Anual.no2_perc50).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc50.isnot(None)
        ).order_by(VNo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no2_perc50)} for r in registros]

    elif submetrica == "NO2 - Percentil 90":
        registros = db.query(VNo2Anual.anio, VNo2Anual.no2_perc90).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc90.isnot(None)
        ).order_by(VNo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no2_perc90)} for r in registros]

    elif submetrica == "NO2 - Percentil 95":
        registros = db.query(VNo2Anual.anio, VNo2Anual.no2_perc95).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc95.isnot(None)
        ).order_by(VNo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no2_perc95)} for r in registros]

    elif submetrica == "NO2 - Percentil 98":
        registros = db.query(VNo2Anual.anio, VNo2Anual.no2_perc98).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc98.isnot(None)
        ).order_by(VNo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no2_perc98)} for r in registros]

    elif submetrica == "NO2 - Percentil 99":
        registros = db.query(VNo2Anual.anio, VNo2Anual.no2_perc99).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc99.isnot(None)
        ).order_by(VNo2Anual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no2_perc99)} for r in registros]

    elif submetrica == "NO2 - Media Mensual":
        registros = db.query(VNo2Mensual.mes, VNo2Mensual.no2_med_mens).filter(
            VNo2Mensual.estacion == estacion.nombre,
            VNo2Mensual.no2_med_mens.isnot(None)
        ).order_by(VNo2Mensual.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.no2_med_mens)} for r in registros]

    # ====================
    # CONTAMINANTES - CO (MONÓXIDO DE CARBONO)
    # ====================
    elif submetrica == "CO - Máximo Horario Anual":
        registros = db.query(VCoAnual.anio, VCoAnual.co_max_hor_anual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_max_hor_anual.isnot(None)
        ).order_by(VCoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.co_max_hor_anual)} for r in registros]

    elif submetrica == "CO - Mínimo Horario Anual":
        registros = db.query(VCoAnual.anio, VCoAnual.co_min_hor_anual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_min_hor_anual.isnot(None)
        ).order_by(VCoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.co_min_hor_anual)} for r in registros]

    elif submetrica == "CO - Percentil 50":
        registros = db.query(VCoAnual.anio, VCoAnual.co_perc50).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc50.isnot(None)
        ).order_by(VCoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.co_perc50)} for r in registros]

    elif submetrica == "CO - Percentil 90":
        registros = db.query(VCoAnual.anio, VCoAnual.co_perc90).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc90.isnot(None)
        ).order_by(VCoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.co_perc90)} for r in registros]

    elif submetrica == "CO - Percentil 95":
        registros = db.query(VCoAnual.anio, VCoAnual.co_perc95).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc95.isnot(None)
        ).order_by(VCoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.co_perc95)} for r in registros]

    elif submetrica == "CO - Percentil 98":
        registros = db.query(VCoAnual.anio, VCoAnual.co_perc98).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc98.isnot(None)
        ).order_by(VCoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.co_perc98)} for r in registros]

    elif submetrica == "CO - Percentil 99":
        registros = db.query(VCoAnual.anio, VCoAnual.co_perc99).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc99.isnot(None)
        ).order_by(VCoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.co_perc99)} for r in registros]

    elif submetrica == "CO - Media Mensual":
        registros = db.query(VCoMensual.mes, VCoMensual.co_med_mens).filter(
            VCoMensual.estacion == estacion.nombre,
            VCoMensual.co_med_mens.isnot(None)
        ).order_by(VCoMensual.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.co_med_mens)} for r in registros]

    # ====================
    # CONTAMINANTES - NO (MONÓXIDO DE NITRÓGENO)
    # ====================
    elif submetrica == "NO - Máximo Horario Anual":
        registros = db.query(VNoAnual.anio, VNoAnual.no_max_hor_anual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_max_hor_anual.isnot(None)
        ).order_by(VNoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no_max_hor_anual)} for r in registros]

    elif submetrica == "NO - Mínimo Horario Anual":
        registros = db.query(VNoAnual.anio, VNoAnual.no_min_hor_anual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_min_hor_anual.isnot(None)
        ).order_by(VNoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no_min_hor_anual)} for r in registros]

    elif submetrica == "NO - Percentil 50":
        registros = db.query(VNoAnual.anio, VNoAnual.no_perc50).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc50.isnot(None)
        ).order_by(VNoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no_perc50)} for r in registros]

    elif submetrica == "NO - Percentil 90":
        registros = db.query(VNoAnual.anio, VNoAnual.no_perc90).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc90.isnot(None)
        ).order_by(VNoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no_perc90)} for r in registros]

    elif submetrica == "NO - Percentil 95":
        registros = db.query(VNoAnual.anio, VNoAnual.no_perc95).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc95.isnot(None)
        ).order_by(VNoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no_perc95)} for r in registros]

    elif submetrica == "NO - Percentil 98":
        registros = db.query(VNoAnual.anio, VNoAnual.no_perc98).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc98.isnot(None)
        ).order_by(VNoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no_perc98)} for r in registros]

    elif submetrica == "NO - Percentil 99":
        registros = db.query(VNoAnual.anio, VNoAnual.no_perc99).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc99.isnot(None)
        ).order_by(VNoAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.no_perc99)} for r in registros]

    elif submetrica == "NO - Media Mensual":
        registros = db.query(VNoMensual.mes, VNoMensual.no_med_mens).filter(
            VNoMensual.estacion == estacion.nombre,
            VNoMensual.no_med_mens.isnot(None)
        ).order_by(VNoMensual.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.no_med_mens)} for r in registros]

    # ====================
    # CONTAMINANTES - NOX (ÓXIDOS DE NITRÓGENO)
    # ====================
    elif submetrica == "NOX - Máximo Horario Anual":
        registros = db.query(VNoxAnual.anio, VNoxAnual.nox_max_hor_anual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_max_hor_anual.isnot(None)
        ).order_by(VNoxAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.nox_max_hor_anual)} for r in registros]

    elif submetrica == "NOX - Mínimo Horario Anual":
        registros = db.query(VNoxAnual.anio, VNoxAnual.nox_min_hor_anual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_min_hor_anual.isnot(None)
        ).order_by(VNoxAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.nox_min_hor_anual)} for r in registros]

    elif submetrica == "NOX - Percentil 50":
        registros = db.query(VNoxAnual.anio, VNoxAnual.nox_perc50).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc50.isnot(None)
        ).order_by(VNoxAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.nox_perc50)} for r in registros]

    elif submetrica == "NOX - Percentil 90":
        registros = db.query(VNoxAnual.anio, VNoxAnual.nox_perc90).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc90.isnot(None)
        ).order_by(VNoxAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.nox_perc90)} for r in registros]

    elif submetrica == "NOX - Percentil 95":
        registros = db.query(VNoxAnual.anio, VNoxAnual.nox_perc95).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc95.isnot(None)
        ).order_by(VNoxAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.nox_perc95)} for r in registros]

    elif submetrica == "NOX - Percentil 98":
        registros = db.query(VNoxAnual.anio, VNoxAnual.nox_perc98).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc98.isnot(None)
        ).order_by(VNoxAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.nox_perc98)} for r in registros]

    elif submetrica == "NOX - Percentil 99":
        registros = db.query(VNoxAnual.anio, VNoxAnual.nox_perc99).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc99.isnot(None)
        ).order_by(VNoxAnual.anio).all()
        datos = [{"periodo": str(r.anio), "valor": float(r.nox_perc99)} for r in registros]

    elif submetrica == "NOX - Media Mensual":
        registros = db.query(VNoxMensual.mes, VNoxMensual.nox_med_mens).filter(
            VNoxMensual.estacion == estacion.nombre,
            VNoxMensual.nox_med_mens.isnot(None)
        ).order_by(VNoxMensual.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.nox_med_mens)} for r in registros]

    # ====================
    # EVENTOS DE OLAS DE CALOR
    # ====================
    elif submetrica == "Número de Eventos de Olas de Calor":
        registros = db.query(VNumEventosDeOlasDeCalor.mes, VNumEventosDeOlasDeCalor.num_eventos_de_olas_de_calor).filter(
            VNumEventosDeOlasDeCalor.estacion == estacion.nombre,
            VNumEventosDeOlasDeCalor.num_eventos_de_olas_de_calor.isnot(None)
        ).order_by(VNumEventosDeOlasDeCalor.mes).all()
        datos = [{"periodo": r.mes, "valor": float(r.num_eventos_de_olas_de_calor)} for r in registros]

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Submétrica '{submetrica}' no reconocida. Verifique el nombre exacto."
        )

    return {
        "nombre": estacion.nombre,
        "submetrica": submetrica,
        "datos": datos
    }

@router.get("/regiones", response_model=List[RegionSchema])
async def get_regiones_disponibles(db: Session = Depends(get_db)):
    """Obtener lista única de regiones que tienen estaciones con datos"""
    regiones = db.query(
        Estacion.numero_region,
        Estacion.nombre_region
    ).distinct().order_by(Estacion.numero_region).all()

    return [
        {"numero_region": r.numero_region, "nombre_region": r.nombre_region}
        for r in regiones
    ]

@router.get("/", response_model=List[EstacionSchema])
async def get_all_estaciones(
    db: Session = Depends(get_db),
    numero_region: Optional[int] = Query(None, description="Filtrar por número de región")
):
    """Obtener todas las estaciones. Opcionalmente filtrar por región."""
    query = db.query(Estacion)

    if numero_region is not None:
        query = query.filter(Estacion.numero_region == numero_region)

    estaciones = query.order_by(Estacion.nombre).all()
    return estaciones

@router.get("/{nombre}", response_model=EstacionSchema)
async def get_estacion_by_nombre(nombre: str, db: Session = Depends(get_db)):
    """Obtener una estación específica por nombre"""
    estacion = db.query(Estacion).filter(Estacion.nombre == nombre).first()
    if not estacion:
        raise HTTPException(status_code=404, detail=f"Estación '{nombre}' no encontrada")
    return estacion

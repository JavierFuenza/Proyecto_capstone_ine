from .aire import (
    VTemperatura, VHumedadRadiacionUV,
    VMp25Anual, VMp25Mensual,
    VMp10Anual, VMp10Mensual,
    VO3Anual, VO3Mensual,
    VSo2Anual, VSo2Mensual,
    VNo2Anual, VNo2Mensual,
    VCoAnual, VCoMensual,
    VNoAnual, VNoMensual,
    VNoxAnual, VNoxMensual,
    VNumEventosDeOlasDeCalor,
)
from .agua import (
    VMarMensual,
    VGlaciaresAnualCuenca,
    VColiformesFecalesEnMatrizBiologica,
    VColiformesFecalesEnMatrizAcuosa,
    VMetalesTotalesEnLaMatrizSedimentaria,
    VMetalesDisueltosEnLaMatrizAcuosa,
    VCaudalMedioDeAguasCorrientes,
    VCantidadDeAguaCaida,
    VEvaporacionRealPorEstacion,
    VVolumenDelEmbalsePorEmbalse,
    VAlturaNieveEquivalenteEnAgua,
    VNivelEstaticoDeAguasSubterraneas,
)
from .estaciones import Estacion
from .entidades_agua import EntidadAgua

__all__ = [
    # Modelos para routers especializados (ahora apuntan a vistas)
    "Estacion",
    "EntidadAgua",

    # AIRE - Vistas
    "VTemperatura",
    "VHumedadRadiacionUV",
    "VNumEventosDeOlasDeCalor",

    # AIRE (Contaminantes Atmosféricos) - Vistas
    "VMp25Anual", "VMp25Mensual",
    "VMp10Anual", "VMp10Mensual",
    "VO3Anual",  "VO3Mensual",
    "VSo2Anual", "VSo2Mensual",
    "VNo2Anual", "VNo2Mensual",
    "VCoAnual",  "VCoMensual",
    "VNoAnual", "VNoMensual",
    "VNoxAnual", "VNoxMensual",

    # AGUA - Vistas Principales
    "VMarMensual",
    "VGlaciaresAnualCuenca",

    # AGUA - Vistas de Datos
    "VColiformesFecalesEnMatrizBiologica",
    "VColiformesFecalesEnMatrizAcuosa",
    "VMetalesTotalesEnLaMatrizSedimentaria",
    "VMetalesDisueltosEnLaMatrizAcuosa",
    "VCaudalMedioDeAguasCorrientes",
    "VCantidadDeAguaCaida",
    "VEvaporacionRealPorEstacion",
    "VVolumenDelEmbalsePorEmbalse",
    "VAlturaNieveEquivalenteEnAgua",
    "VNivelEstaticoDeAguasSubterraneas",
]

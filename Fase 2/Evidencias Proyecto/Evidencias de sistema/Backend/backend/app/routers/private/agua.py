from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from core.dependencies import get_db
from models.agua import *
from schemas.agua import *

# Crear sub-routers para organizar endpoints por categoría
vistas_router = APIRouter(
    prefix="/agua/vistas",
    tags=["Agua - Vistas Generales"],
    responses={404: {"description": "No encontrado"}}
)

contaminantes_router = APIRouter(
    prefix="/agua/contaminantes",
    tags=["Agua - Contaminantes"],
    responses={404: {"description": "No encontrado"}}
)

hidrologia_router = APIRouter(
    prefix="/agua/hidrologia",
    tags=["Agua - Hidrología"],
    responses={404: {"description": "No encontrado"}}
)

meteorologicos_router = APIRouter(
    prefix="/agua/meteorologicos",
    tags=["Agua - Meteorológicos"],
    responses={404: {"description": "No encontrado"}}
)

almacenamiento_router = APIRouter(
    prefix="/agua/almacenamiento",
    tags=["Agua - Almacenamiento"],
    responses={404: {"description": "No encontrado"}}
)

# Router principal para incluir en main.py
router = APIRouter()

# ============================
# ENDPOINTS - VISTAS GENERALES
# ============================

@vistas_router.get(
    "/mar-mensual",
    response_model=List[MarMensualSchema],
    summary="Datos mensuales del océano",
    description="Temperatura superficial y nivel medio del mar en estaciones costeras de Chile."
)
async def get_mar_mensual(db: Session = Depends(get_db)):
    """
    Obtiene datos mensuales oceanográficos de estaciones costeras.

    **Datos incluidos:**
    - Temperatura superficial del mar (°C)
    - Nivel medio del mar (cm)

    **Periodo:** Datos desde 2015 hasta la actualidad

    **Estaciones:** Arica, Antofagasta, Caldera, Coquimbo, Valparaíso, San Antonio,
    Talcahuano, Corral, Puerto Montt, entre otras.

    **Importancia:** El nivel del mar y su temperatura son indicadores clave del cambio climático.
    El aumento del nivel del mar amenaza zonas costeras, mientras que cambios en la temperatura
    afectan ecosistemas marinos y pesquerías.

    **Fuente:** SHOA (Servicio Hidrográfico y Oceanográfico de la Armada de Chile)
    """
    data = db.query(VMarMensual).order_by(VMarMensual.mes).all()
    return data

@vistas_router.get(
    "/glaciares-anual-cuenca",
    response_model=List[GlaciaresAnualCuencaSchema],
    summary="Datos anuales de glaciares",
    description="Estadísticas de glaciares por cuenca hidrográfica en Chile."
)
async def get_glaciares_anual_cuenca(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas anuales de glaciares por cuenca hidrográfica.

    **Datos incluidos:**
    - Número de glaciares por cuenca
    - Superficie total de glaciares (km²)
    - Volumen estimado de hielo glaciar (km³)
    - Volumen estimado de agua equivalente (km³)

    **Periodo:** Datos desde 2013 hasta la actualidad

    **Cuencas hidrográficas:** Incluye todas las principales cuencas de Chile, desde
    Altiplánicas en el norte hasta Tierra del Fuego en el sur.

    **Importancia:** Los glaciares son reservas críticas de agua dulce. Chile contiene
    aproximadamente 24,000 km² de glaciares, representando el 82% de los glaciares de
    Sudamérica. Su retroceso por el cambio climático amenaza el suministro de agua para
    consumo humano, agricultura e hidroelectricidad.

    **Fuente:** DGA (Dirección General de Aguas) - Inventario Público de Glaciares
    """
    data = db.query(VGlaciaresAnualCuenca).order_by(VGlaciaresAnualCuenca.anio).all()
    return data

# ============================
# ENDPOINTS - CONTAMINANTES DEL AGUA
# ============================

@contaminantes_router.get(
    "/coliformes-biologica",
    response_model=List[ColiformesBiologicaSchema],
    summary="Coliformes fecales en matriz biológica",
    description="Concentraciones de coliformes fecales en organismos marinos (mejillones, machas, etc.)."
)
async def get_coliformes_biologica(db: Session = Depends(get_db)):
    """
    Obtiene mediciones de coliformes fecales en organismos marinos.

    **Coliformes Fecales:** Bacterias indicadoras de contaminación fecal. Su presencia
    en organismos marinos indica contaminación del agua por aguas servidas.

    **Datos incluidos:**
    - Fecha de medición
    - Estación de monitoreo (Red POAL)
    - Concentración (NMP/100g - Número Más Probable por 100 gramos)

    **Periodo:** Datos desde 2015 hasta la actualidad

    **Matriz biológica:** Organismos filtradores como mejillones y machas que acumulan
    contaminantes del agua.

    **Norma sanitaria:** Límite máximo 230 NMP/100g para consumo humano (según Reglamento
    Sanitario de los Alimentos).

    **Importancia:** Monitoreo crucial para seguridad alimentaria y salud pública en
    zonas de extracción de mariscos.

    **Fuente:** Red POAL (Programa de Observación del Ambiente Litoral) - IFOP
    """
    data = db.query(VColiformesFecalesEnMatrizBiologica).order_by(VColiformesFecalesEnMatrizBiologica.dia).all()
    return data

@contaminantes_router.get(
    "/coliformes-acuosa",
    response_model=List[ColiformesAcuosaSchema],
    summary="Coliformes fecales en agua de mar",
    description="Concentraciones de coliformes fecales en agua marina costera."
)
async def get_coliformes_acuosa(db: Session = Depends(get_db)):
    """
    Obtiene mediciones de coliformes fecales en agua de mar.

    **Datos incluidos:**
    - Fecha de medición
    - Estación de monitoreo (Red POAL)
    - Concentración (NMP/100mL - Número Más Probable por 100 mililitros)

    **Periodo:** Datos desde 2015 hasta la actualidad

    **Norma para balnearios:** Límite máximo 1,000 NMP/100mL para aguas aptas para
    recreación con contacto directo (D.S. N° 144/2008).

    **Importancia:** Indicador de calidad de agua para balnearios y zonas de recreación
    costera. La contaminación fecal puede transmitir enfermedades gastrointestinales.

    **Fuente:** Red POAL - IFOP
    """
    data = db.query(VColiformesFecalesEnMatrizAcuosa).order_by(VColiformesFecalesEnMatrizAcuosa.dia).all()
    return data

@contaminantes_router.get(
    "/metales-sedimentaria",
    response_model=List[MetalesSedimentariaSchema],
    summary="Metales pesados en sedimentos marinos",
    description="Concentraciones de metales totales en sedimentos costeros."
)
async def get_metales_sedimentaria(db: Session = Depends(get_db)):
    """
    Obtiene concentraciones de metales pesados en sedimentos marinos.

    **Metales analizados:** Arsénico (As), Cadmio (Cd), Cobre (Cu), Cromo (Cr),
    Mercurio (Hg), Níquel (Ni), Plomo (Pb), Zinc (Zn), entre otros.

    **Datos incluidos:**
    - Fecha de medición
    - Estación de monitoreo (Red POAL)
    - Parámetro (tipo de metal)
    - Concentración (mg/kg peso seco)

    **Periodo:** Datos desde 2015 hasta la actualidad

    **Importancia:** Los sedimentos marinos actúan como sumideros de contaminantes.
    Los metales pesados se acumulan en sedimentos y pueden ser liberados al agua,
    ingresando a la cadena alimentaria marina. Monitoreo crucial en zonas con actividad
    minera, industrial y portuaria.

    **Efectos:** Toxicidad para organismos marinos, bioacumulación en peces y mariscos,
    riesgos para salud humana por consumo.

    **Fuente:** Red POAL - IFOP
    """
    data = db.query(VMetalesTotalesEnLaMatrizSedimentaria).order_by(VMetalesTotalesEnLaMatrizSedimentaria.dia).all()
    return data

@contaminantes_router.get(
    "/metales-acuosa",
    response_model=List[MetalesAcuosaSchema],
    summary="Metales pesados disueltos en agua",
    description="Concentraciones de metales disueltos en agua marina costera."
)
async def get_metales_acuosa(db: Session = Depends(get_db)):
    """
    Obtiene concentraciones de metales pesados disueltos en agua de mar.

    **Metales analizados:** Arsénico, Cadmio, Cobre, Cromo, Mercurio, Níquel, Plomo, Zinc.

    **Datos incluidos:**
    - Fecha de medición
    - Estación de monitoreo (Red POAL)
    - Parámetro (tipo de metal)
    - Concentración (µg/L - microgramos por litro)

    **Periodo:** Datos desde 2015 hasta la actualidad

    **Diferencia con matriz sedimentaria:** Los metales disueltos están biodisponibles,
    es decir, pueden ser absorbidos directamente por organismos marinos.

    **Norma:** D.S. N° 144/2008 establece límites de metales para protección de vida acuática.

    **Fuente:** Red POAL - IFOP
    """
    data = db.query(VMetalesDisueltosEnLaMatrizAcuosa).order_by(VMetalesDisueltosEnLaMatrizAcuosa.dia).all()
    return data

# ============================
# ENDPOINTS - HIDROLOGÍA
# ============================

@hidrologia_router.get(
    "/caudal",
    response_model=List[CaudalSchema],
    summary="Caudal de ríos",
    description="Caudal medio mensual en estaciones fluviométricas de Chile."
)
async def get_caudal(db: Session = Depends(get_db)):
    """
    Obtiene mediciones de caudal medio mensual en ríos y esteros de Chile.

    **Datos incluidos:**
    - Mes del registro
    - Nombre del río o estero
    - Estación fluviométrica
    - Caudal medio mensual (m³/s - metros cúbicos por segundo)

    **Periodo:** Datos desde 2013 hasta la actualidad

    **Red de monitoreo:** Más de 400 estaciones fluviométricas distribuidas en todo Chile.

    **Principales ríos monitoreados:** Loa, Elqui, Limarí, Aconcagua, Maipo, Maule,
    Biobío, Imperial, Toltén, Valdivia, Bueno, Puelo, Baker, entre muchos otros.

    **Importancia:** El caudal de los ríos es fundamental para:
    - Gestión de recursos hídricos
    - Planificación de riego agrícola
    - Generación hidroeléctrica
    - Abastecimiento de agua potable
    - Prevención de sequías e inundaciones

    **Tendencias:** Chile enfrenta una megasequía desde 2010, con reducciones significativas
    en caudales, especialmente en zona centro-sur.

    **Fuente:** DGA (Dirección General de Aguas) - Red Hidrométrica Nacional
    """
    data = db.query(VCaudalMedioDeAguasCorrientes).order_by(VCaudalMedioDeAguasCorrientes.mes).all()
    return data

@hidrologia_router.get(
    "/pozos",
    response_model=List[PozoSchema],
    summary="Nivel de aguas subterráneas",
    description="Nivel estático de aguas subterráneas en pozos de monitoreo."
)
async def get_pozos(db: Session = Depends(get_db)):
    """
    Obtiene mediciones del nivel estático de aguas subterráneas.

    **Nivel estático:** Profundidad desde la superficie del suelo hasta el nivel del agua
    en el pozo, cuando el pozo no está siendo bombeado.

    **Datos incluidos:**
    - Fecha de medición
    - Estación de monitoreo (pozo)
    - Nivel estático (metros bajo el nivel del suelo)

    **Periodo:** Datos desde 2014 hasta la actualidad

    **Importancia:** Las aguas subterráneas son fuente crítica de agua para:
    - Consumo humano en zonas rurales
    - Riego agrícola (60% del agua de riego en Chile)
    - Procesos industriales y mineros

    **Sobreexplotación:** Muchos acuíferos en Chile están bajo estrés hídrico, con niveles
    descendiendo consistentemente debido a extracción excesiva y sequía prolongada.

    **Zonas críticas:** Valle de Copiapó, Petorca, Ligua, La Ligua-Petorca declaradas
    zonas de escasez hídrica.

    **Fuente:** DGA - Red de Monitoreo de Aguas Subterráneas
    """
    data = db.query(VNivelEstaticoDeAguasSubterraneas).order_by(VNivelEstaticoDeAguasSubterraneas.dia).all()
    return data

# ============================
# ENDPOINTS - METEOROLÓGICOS HÍDRICOS
# ============================

@meteorologicos_router.get(
    "/lluvia",
    response_model=List[LluviaSchema],
    summary="Precipitaciones",
    description="Precipitación mensual acumulada en estaciones meteorológicas."
)
async def get_lluvia(db: Session = Depends(get_db)):
    """
    Obtiene datos de precipitación mensual acumulada.

    **Datos incluidos:**
    - Mes del registro
    - Estación meteorológica
    - Precipitación acumulada mensual (mm - milímetros)

    **Periodo:** Datos desde 2010 hasta la actualidad

    **Red de monitoreo:** Más de 100 estaciones meteorológicas DMC en todo Chile.

    **Gradiente de precipitaciones:** Chile presenta extrema variabilidad:
    - **Norte:** Desierto de Atacama - precipitación casi nula (<10 mm/año)
    - **Centro:** Clima mediterráneo - 300-1000 mm/año concentrado en invierno
    - **Sur:** Clima templado lluvioso - 1500-4000 mm/año distribuido todo el año
    - **Patagonia:** Alta variabilidad, 400-5000 mm/año según ubicación

    **Sequía:** Chile central enfrenta déficit de precipitaciones desde 2010, con
    reducciones del 20-40% respecto a valores históricos.

    **Importancia:** La precipitación determina disponibilidad hídrica para todos los usos:
    agricultura, generación hidroeléctrica, ecosistemas, consumo humano.

    **Fuente:** DMC (Dirección Meteorológica de Chile)
    """
    data = db.query(VCantidadDeAguaCaida).order_by(VCantidadDeAguaCaida.mes).all()
    return data

@meteorologicos_router.get(
    "/evaporacion",
    response_model=List[EvaporacionSchema],
    summary="Evaporación real",
    description="Evaporación real mensual en estaciones meteorológicas."
)
async def get_evaporacion(db: Session = Depends(get_db)):
    """
    Obtiene datos de evaporación real mensual.

    **Evaporación real:** Cantidad de agua que efectivamente se evapora desde superficies
    de agua, suelo y vegetación hacia la atmósfera.

    **Datos incluidos:**
    - Mes del registro
    - Estación meteorológica
    - Evaporación real mensual (mm - milímetros)

    **Periodo:** Datos desde 2013 hasta la actualidad

    **Importancia:** La evaporación es componente crítico del balance hídrico:
    - **Balance hídrico = Precipitación - Evaporación - Escorrentía**
    - Determina cuánta agua queda disponible para usos humanos y ecosistemas
    - Afecta eficiencia de riego agrícola
    - Influye en niveles de embalses y humedales

    **Factores que afectan evaporación:**
    - Temperatura del aire
    - Radiación solar
    - Humedad relativa
    - Velocidad del viento

    **Cambio climático:** El aumento de temperaturas está incrementando tasas de evaporación,
    agravando estrés hídrico incluso en zonas con precipitaciones constantes.

    **Fuente:** DGA / DMC
    """
    data = db.query(VEvaporacionRealPorEstacion).order_by(VEvaporacionRealPorEstacion.mes).all()
    return data

@meteorologicos_router.get(
    "/nieve",
    response_model=List[NieveSchema],
    summary="Nieve acumulada",
    description="Altura de nieve equivalente en agua en estaciones nivométricas."
)
async def get_nieve(db: Session = Depends(get_db)):
    """
    Obtiene mediciones de altura de nieve expresada como equivalente en agua.

    **Equivalente en agua:** Altura de agua líquida que se obtendría si se derritiera
    completamente la capa de nieve. Aproximadamente, 10 cm de nieve = 1 cm de agua.

    **Datos incluidos:**
    - Fecha de medición
    - Estación nivométrica
    - Altura nieve equivalente en agua (mm)

    **Periodo:** Datos desde 2015 hasta la actualidad

    **Estaciones nivométricas:** Ubicadas en cordillera de Los Andes y Cordillera de
    la Costa, desde Región de Coquimbo hasta Región de Los Lagos.

    **Importancia crítica para Chile:**

    La nieve cordillerana es el **principal reservorio de agua dulce** de Chile:
    - Actúa como "embalse natural" que almacena agua en invierno
    - Se derrite gradualmente en primavera-verano, alimentando ríos
    - Proporciona hasta el 80% del agua disponible en Chile central
    - Fundamental para riego agrícola en temporada de mayor demanda
    - Alimenta generación hidroeléctrica
    - Mantiene ecosistemas y biodiversidad

    **Crisis actual:** La nieve en Los Andes ha disminuido significativamente:
    - Reducción del 25-50% en acumulación respecto a promedio histórico
    - Temporada de deshielo adelantada por aumento de temperaturas
    - Menor altitud de línea de nieve (más lluvia, menos nieve)

    **Fuente:** DGA - Red Nivométrica Nacional
    """
    data = db.query(VAlturaNieveEquivalenteEnAgua).order_by(VAlturaNieveEquivalenteEnAgua.dia).all()
    return data

# ============================
# ENDPOINTS - ALMACENAMIENTO DE AGUA
# ============================

@almacenamiento_router.get(
    "/embalses",
    response_model=List[EmbalseSchema],
    summary="Volumen de embalses",
    description="Volumen mensual almacenado en embalses y lagos artificiales de Chile."
)
async def get_embalses(db: Session = Depends(get_db)):
    """
    Obtiene datos mensuales de volumen almacenado en embalses.

    **Datos incluidos:**
    - Mes del registro
    - Nombre del embalse
    - Volumen almacenado (millones de m³)

    **Periodo:** Datos desde 2010 hasta la actualidad

    **Principales embalses monitoreados:**
    - **Zona Norte:** Conchi, Santa Juana, Lautaro
    - **Zona Central:** El Yeso, Laguna Negra, Rapel, Colbún, Maule
    - **Zona Sur:** Ralco, Pangue, Chapo, Laja

    **Usos del agua embalsada:**
    - **Riego agrícola** (uso dominante en zona central)
    - **Generación hidroeléctrica** (embalses como Ralco, Colbún, Laja)
    - **Agua potable** (El Yeso para Santiago)
    - **Control de crecidas**
    - **Regulación de caudales**

    **Capacidad total:** Chile tiene aproximadamente 70 embalses con capacidad total
    superior a 4,000 millones de m³.

    **Crisis hídrica:** Durante la megasequía (2010-actualidad), muchos embalses han
    operado bajo 50% de su capacidad, algunos alcanzando mínimos históricos.

    **Embalses críticos:** El Yeso (principal fuente de agua potable de Santiago) y
    embalses de riego en zona central han presentado niveles históricamente bajos.

    **Importancia estratégica:** Los embalses son infraestructura crítica para seguridad
    hídrica, permitiendo almacenar agua de años húmedos para años secos.

    **Fuente:** DGA - Monitoreo de Embalses
    """
    data = db.query(VVolumenDelEmbalsePorEmbalse).order_by(VVolumenDelEmbalsePorEmbalse.mes).all()
    return data

# Incluir sub-routers en el router principal
router.include_router(vistas_router)
router.include_router(contaminantes_router)
router.include_router(hidrologia_router)
router.include_router(meteorologicos_router)
router.include_router(almacenamiento_router)

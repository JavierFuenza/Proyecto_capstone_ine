from sqlalchemy import Column, String, Float, BigInteger, Text
from core.database import Base

# ============================
# Vista de Mar (lowercase clean columns)
# ============================
class VMarMensual(Base):
    __tablename__ = "v_mar_mensual"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    temp_superficial_del_mar = Column(Float)
    nivel_medio_del_mar = Column(Float)

# ============================
# Vista de Glaciares (lowercase clean columns)
# ============================
class VGlaciaresAnualCuenca(Base):
    __tablename__ = "v_glaciares_anual_cuenca"
    __table_args__ = {"schema": "public"}

    anio = Column(BigInteger, primary_key=True)
    estacion = Column(Text, primary_key=True)

    num_glaciares_por_cuenca = Column(BigInteger)
    superficie_de_glaciares_por_cuenca = Column(Float)
    volumen_de_hielo_glaciar_estimado_por_cuenca = Column(Float)
    volumen_de_agua_de_glaciares_estimada_por_cuenca = Column(Float)

# ============================
# Vista: Coliformes Biológica
# ============================
class VColiformesFecalesEnMatrizBiologica(Base):
    __tablename__ = "v_coliformes_fecales_en_matriz_biologica"
    __table_args__ = {"schema": "public"}

    dia = Column("Día", Text, primary_key=True)
    estaciones_poal = Column("Estaciones POAL", Text, primary_key=True)
    value = Column("Value", BigInteger)

# ============================
# Vista: Coliformes Acuosa
# ============================
class VColiformesFecalesEnMatrizAcuosa(Base):
    __tablename__ = "v_coliformes_fecales_en_matriz_acuosa"
    __table_args__ = {"schema": "public"}

    dia = Column("Día", Text, primary_key=True)
    estaciones_poal = Column("Estaciones POAL", Text, primary_key=True)
    value = Column("Value", Float)

# ============================
# Vista: Metales Sedimentaria
# ============================
class VMetalesTotalesEnLaMatrizSedimentaria(Base):
    __tablename__ = "v_metales_totales_en_la_matriz_sedimentaria"
    __table_args__ = {"schema": "public"}

    dia = Column("Día", Text, primary_key=True)
    estaciones_poal = Column("Estaciones POAL", Text, primary_key=True)
    parametros_poal = Column("Parámetros POAL", Text, primary_key=True)
    value = Column("Value", Float)

# ============================
# Vista: Metales Acuosa
# ============================
class VMetalesDisueltosEnLaMatrizAcuosa(Base):
    __tablename__ = "v_metales_disueltos_en_la_matriz_acuosa"
    __table_args__ = {"schema": "public"}

    dia = Column("Día", Text, primary_key=True)
    estaciones_poal = Column("Estaciones POAL", Text, primary_key=True)
    parametros_poal = Column("Parámetros POAL", Text, primary_key=True)
    value = Column("Value", Float)

# ============================
# Vista: Caudal
# ============================
class VCaudalMedioDeAguasCorrientes(Base):
    __tablename__ = "v_caudal_medio_de_aguas_corrientes"
    __table_args__ = {"schema": "public"}

    mes = Column("Mes", Text, primary_key=True)
    aguas_corrientes = Column("Aguas Corrientes", Text, primary_key=True)
    estaciones_fluviometricas = Column("Estaciones Fluviométricas", Text, primary_key=True)
    value = Column("Value", Float)

# ============================
# Vista: Lluvia
# ============================
class VCantidadDeAguaCaida(Base):
    __tablename__ = "v_cantidad_de_agua_caida"
    __table_args__ = {"schema": "public"}

    mes = Column("Mes", Text, primary_key=True)
    estaciones_meteorologicas_dmc = Column("Estaciones meteorológicas DMC", Text, primary_key=True)
    value = Column("Value", Float)

# ============================
# Vista: Evaporación
# ============================
class VEvaporacionRealPorEstacion(Base):
    __tablename__ = "v_evaporacion_real_por_estacion"
    __table_args__ = {"schema": "public"}

    mes = Column("Mes", Text, primary_key=True)
    estacion = Column("Estación", Text, primary_key=True)
    value = Column("Value", Float)

# ============================
# Vista: Embalses
# ============================
class VVolumenDelEmbalsePorEmbalse(Base):
    __tablename__ = "v_volumen_del_embalse_por_embalse"
    __table_args__ = {"schema": "public"}

    mes = Column("Mes", Text, primary_key=True)
    embalse = Column("Embalse", Text, primary_key=True)
    value = Column("Value", Float)

# ============================
# Vista: Nieve
# ============================
class VAlturaNieveEquivalenteEnAgua(Base):
    __tablename__ = "v_altura_nieve_equivalente_en_agua"
    __table_args__ = {"schema": "public"}

    dia = Column("Día", Text, primary_key=True)
    estaciones_nivometricas = Column("Estaciones nivométricas", Text, primary_key=True)
    value = Column("Value", BigInteger)

# ============================
# Vista: Pozos
# ============================
class VNivelEstaticoDeAguasSubterraneas(Base):
    __tablename__ = "v_nivel_estatico_de_aguas_subterraneas"
    __table_args__ = {"schema": "public"}

    dia = Column("Día", Text, primary_key=True)
    estaciones_pozo = Column("Estaciones Pozo", Text, primary_key=True)
    value = Column("Value", Float)

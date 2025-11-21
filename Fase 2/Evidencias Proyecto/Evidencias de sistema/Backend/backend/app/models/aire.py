from sqlalchemy import Column, String, Float, BigInteger, Text
from core.database import Base

# ============================
# Vista Temperatura
# ============================
class VTemperatura(Base):
    __tablename__ = "v_temperatura"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    temp_max_absoluta = Column(Float)
    temp_min_absoluta = Column(Float)
    temp_max_med = Column(Float)
    temp_min_med = Column(Float)
    temp_med = Column(Float)

# ============================
# Vista Humedad, Radiación y UV
# ============================
class VHumedadRadiacionUV(Base):
    __tablename__ = "v_humedad_radiacion_uv"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    humedad_rel_med_mens = Column(Float)
    rad_global_med = Column(Float)  # Cambio: en el esquema es double precision
    uvb_prom = Column(Float)

# ============================
# Vistas MP25
# ============================
class VMp25Anual(Base):
    __tablename__ = "v_mp25_anual"
    __table_args__ = {"schema": "public"}

    anio = Column(BigInteger, primary_key=True)
    estacion = Column(Text, primary_key=True)

    mp25_max_hor_anual = Column(Float)
    mp25_min_hor_anual = Column(Float)
    mp25_perc50       = Column(Float)
    mp25_perc90       = Column(Float)
    mp25_perc95       = Column(Float)
    mp25_perc98       = Column(Float)  # Cambio: es double precision

class VMp25Mensual(Base):
    __tablename__ = "v_mp25_mensual"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    mp25_med_mens = Column(Float)

# ============================
# Vistas MP10
# ============================
class VMp10Anual(Base):
    __tablename__ = "v_mp10_anual"
    __table_args__ = {"schema": "public"}

    anio = Column(BigInteger, primary_key=True)
    estacion = Column(Text, primary_key=True)

    mp10_max_hor_anual = Column(Float)
    mp10_min_hor_anual = Column(Float)
    mp10_perc50       = Column(Float)
    mp10_perc90       = Column(Float)
    mp10_perc95       = Column(Float)
    mp10_perc98       = Column(Float)  # Cambio: es double precision

class VMp10Mensual(Base):
    __tablename__ = "v_mp10_mensual"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    mp10_med_mens = Column(BigInteger)

# ============================
# Vistas o3
# ============================
class VO3Anual(Base):
    __tablename__ = "v_o3_anual"
    __table_args__ = {"schema": "public"}

    anio = Column(BigInteger, primary_key=True)
    estacion = Column(Text, primary_key=True)

    o3_max_hor_anual = Column(Float)
    o3_min_hor_anual = Column(BigInteger)  # Cambio: es bigint en el esquema
    o3_perc50       = Column(Float)
    o3_perc90       = Column(Float)
    o3_perc95       = Column(Float)
    o3_perc98       = Column(Float)
    o3_perc99       = Column(Float)

class VO3Mensual(Base):
    __tablename__ = "v_o3_mensual"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    o3_med_mens = Column(Float)

# ============================
# Vistas So2
# ============================
class VSo2Anual(Base):
    __tablename__ = "v_so2_anual"
    __table_args__ = {"schema": "public"}

    anio = Column(BigInteger, primary_key=True)
    estacion = Column(Text, primary_key=True)

    so2_max_hor_anual = Column(Float)
    so2_min_anual     = Column(Float)
    so2_perc50        = Column(Float)
    so2_perc90        = Column(Float)
    so2_perc95        = Column(Float)
    so2_perc98        = Column(Float)
    so2_perc99        = Column(Float)

class VSo2Mensual(Base):
    __tablename__ = "v_so2_mensual"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    so2_med_mens = Column(Float)

# ============================
# Vistas No2
# ============================
class VNo2Anual(Base):
    __tablename__ = "v_no2_anual"
    __table_args__ = {"schema": "public"}

    anio = Column(BigInteger, primary_key=True)
    estacion = Column(Text, primary_key=True)

    no2_max_hor_anual = Column(Float)
    no2_min_hor_anual = Column(Float)
    no2_perc50        = Column(Float)
    no2_perc90        = Column(Float)
    no2_perc95        = Column(Float)
    no2_perc98        = Column(Float)
    no2_perc99        = Column(Float)

class VNo2Mensual(Base):
    __tablename__ = "v_no2_mensual"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    no2_med_mens = Column(Float)

# ============================
# Vistas Co
# ============================
class VCoAnual(Base):
    __tablename__ = "v_co_anual"
    __table_args__ = {"schema": "public"}

    anio = Column(BigInteger, primary_key=True)
    estacion = Column(Text, primary_key=True)

    co_max_hor_anual = Column(Float)
    co_min_hor_anual = Column(Float)
    co_perc50        = Column(Float)
    co_perc90        = Column(Float)
    co_perc95        = Column(Float)
    co_perc98        = Column(Float)
    co_perc99        = Column(Float)

class VCoMensual(Base):
    __tablename__ = "v_co_mensual"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    co_med_mens = Column(Float)

# ============================
# Vistas No
# ============================
class VNoAnual(Base):
    __tablename__ = "v_no_anual"
    __table_args__ = {"schema": "public"}

    anio = Column(BigInteger, primary_key=True)
    estacion = Column(Text, primary_key=True)

    no_max_hor_anual = Column(Float)
    no_min_hor_anual = Column(Float)
    no_perc50 = Column(Float)
    no_perc90 = Column(Float)
    no_perc95 = Column(Float)
    no_perc98 = Column(Float)
    no_perc99 = Column(Float)

class VNoMensual(Base):
    __tablename__ = "v_no_mensual"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    no_med_mens = Column(Float)

# ============================
# Vistas NoX
# ============================
class VNoxAnual(Base):
    __tablename__ = "v_nox_anual"
    __table_args__ = {"schema": "public"}

    anio = Column(BigInteger, primary_key=True)
    estacion = Column(Text, primary_key=True)

    nox_max_hor_anual = Column(Float)
    nox_min_hor_anual = Column(Float)
    nox_perc50 = Column(Float)
    nox_perc90 = Column(Float)
    nox_perc95 = Column(Float)
    nox_perc98 = Column(Float)
    nox_perc99 = Column(Float)

class VNoxMensual(Base):
    __tablename__ = "v_nox_mensual"
    __table_args__ = {"schema": "public"}

    mes = Column(Text, primary_key=True)
    estacion = Column(Text, primary_key=True)

    nox_med_mens = Column(Float)

# ============================
# Vista Eventos de Olas de Calor
# ============================
class VNumEventosDeOlasDeCalor(Base):
    __tablename__ = "v_num_eventos_de_olas_de_calor"
    __table_args__ = {"schema": "public"}

    mes = Column(String, primary_key=True)
    estacion = Column(Text, primary_key=True)

    num_eventos_de_olas_de_calor = Column(BigInteger)

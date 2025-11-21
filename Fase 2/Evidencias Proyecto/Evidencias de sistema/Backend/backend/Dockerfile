# Imagen base oficial de Python
FROM python:3.11-slim

# Establecemos directorio de trabajo
WORKDIR /app

# Instalamos dependencias del sistema (opcional, pero recomendado)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos requirements primero (para aprovechar la cache de Docker)
COPY ./app/requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la aplicación
COPY ./app .

# Exponemos el puerto
EXPOSE 8000

# Comando de arranque optimizado
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--reload"]

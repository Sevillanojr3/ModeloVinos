# Imagen base ligera de Python
FROM python:3.10-slim

# Variables de entorno
ENV GRPC_PORT=50051 \
    MODEL_PATH=/app/models/random_forest_model.pkl \
    PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
   gcc \
   python3-dev \
   && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del microservicio
COPY ../../GRP/*.py /app/GRP/
COPY ../../GRP/*.proto /app/GRP/

# Crear directorio para modelos
RUN mkdir -p /app/models

# Puerto gRPC
EXPOSE ${GRPC_PORT}

# Comando para iniciar el servicio
ENTRYPOINT ["python", "-m", "GRP.grp_app"] 
#!/bin/bash

# Definir versión
VERSION="1.0"

echo "🌐 Creando red de microservicios..."
docker network create microservices-net || true

echo "🚀 Iniciando contenedores..."

# Iniciar el microservicio gRPC
docker run -d \
    --name wine-predictor \
    --network microservices-net \
    --network-alias wine-predictor \
    -p 50051:50051 \
    -v "$(pwd)/models:/app/models" \
    -e GRPC_PORT=50051 \
    -e MODEL_PATH=/app/models/random_forest_model.pkl \
    microservicio-grpc:${VERSION}

echo "✅ Servicios iniciados"
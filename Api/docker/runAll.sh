#!/bin/bash

# Definir variables
IMAGE_NAME="fastapi-wine-classifier"
VERSION="1.0"
CONTAINER_NAME="wine-classifier"
NETWORK_NAME="microservices-net"

# Crear red si no existe
echo "Creando red $NETWORK_NAME..."
docker network create $NETWORK_NAME 2>/dev/null || true

# Detener y eliminar contenedor si existe
docker rm -f $CONTAINER_NAME 2>/dev/null || true

# Ejecutar el contenedor
echo "Iniciando contenedor $CONTAINER_NAME..."
docker run -d \
    --name $CONTAINER_NAME \
    --network $NETWORK_NAME \
    -p 8000:8000 \
    -e APP_ENV=production \
    -e APP_PORT=8000 \
    $IMAGE_NAME:$VERSION

echo "Contenedor iniciado exitosamente"
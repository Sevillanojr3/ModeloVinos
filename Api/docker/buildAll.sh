#!/bin/bash

# Definir variables
IMAGE_NAME="fastapi-wine-classifier"
VERSION="1.0"

echo "Construyendo imagen de $IMAGE_NAME:$VERSION..."

# Construir la imagen
docker build -t $IMAGE_NAME:$VERSION .

echo "Construcción completada"
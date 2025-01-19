#!/bin/bash

# Definir versión
VERSION="1.0"

echo "🏗️ Construyendo imágenes Docker..."

# Construir la imagen del microservicio gRPC
docker build -t microservicio-grpc:${VERSION} .

echo "✅ Construcción completada"
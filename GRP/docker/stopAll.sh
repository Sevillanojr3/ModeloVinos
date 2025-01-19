#!/bin/bash

echo "🛑 Deteniendo contenedores..."

# Detener y eliminar el contenedor del microservicio gRPC
docker stop wine-predictor || true
docker rm wine-predictor || true

echo "🧹 Limpiando red..."
docker network rm microservices-net || true

echo "✅ Limpieza completada"
#!/bin/bash

# Detener y eliminar contenedores
echo "Deteniendo contenedores..."
docker stop prediction-service kafka zookeeper 2>/dev/null || true
docker rm prediction-service kafka zookeeper 2>/dev/null || true

# Eliminar red
echo "Eliminando red..."
docker network rm microservices-net 2>/dev/null || true

echo "¡Limpieza completada!"
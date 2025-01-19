#!/bin/bash

# Definir variables
CONTAINER_NAME="wine-classifier"
NETWORK_NAME="microservices-net"

# Detener y eliminar contenedor
echo "Deteniendo contenedor $CONTAINER_NAME..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

# Eliminar red
echo "Eliminando red $NETWORK_NAME..."
docker network rm $NETWORK_NAME 2>/dev/null || true

echo "Limpieza completada"
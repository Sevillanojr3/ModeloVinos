#!/bin/bash

# Construir la imagen del servicio de predicción
echo "Construyendo imagen del servicio de predicción..."
docker build -t microservicio-kafka:1.0 .

# Descargar y construir imagen de Kafka si no existe
if [[ "$(docker images -q confluentinc/cp-kafka:latest 2> /dev/null)" == "" ]]; then
    echo "Descargando imagen de Kafka..."
    docker pull confluentinc/cp-kafka:latest
fi

# Descargar imagen de Zookeeper si no existe
if [[ "$(docker images -q confluentinc/cp-zookeeper:latest 2> /dev/null)" == "" ]]; then
    echo "Descargando imagen de Zookeeper..."
    docker pull confluentinc/cp-zookeeper:latest
fi

echo "Construcción completada!"
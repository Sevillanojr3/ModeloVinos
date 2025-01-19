#!/bin/bash

# Crear red si no existe
docker network create microservices-net 2>/dev/null || true

# Iniciar Zookeeper
echo "Iniciando Zookeeper..."
docker run -d \
    --name zookeeper \
    --network microservices-net \
    -e ZOOKEEPER_CLIENT_PORT=2181 \
    -e ZOOKEEPER_TICK_TIME=2000 \
    confluentinc/cp-zookeeper:latest

# Esperar a que Zookeeper esté listo
sleep 10

# Iniciar Kafka
echo "Iniciando Kafka..."
docker run -d \
    --name kafka \
    --network microservices-net \
    -e KAFKA_BROKER_ID=1 \
    -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 \
    -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    confluentinc/cp-kafka:latest

# Esperar a que Kafka esté listo
sleep 20

# Iniciar el servicio de predicción
echo "Iniciando servicio de predicción..."
docker run -d \
    --name prediction-service \
    --network microservices-net \
    -v $(pwd)/models:/app/models \
    -e KAFKA_BOOTSTRAP_SERVERS=kafka:9092 \
    microservicio-kafka:1.0

echo "¡Servicios iniciados correctamente!"
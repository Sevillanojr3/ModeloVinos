Para ejecutar el sistema de comparación de predicciones, sigue estos pasos en orden:

1. REQUISITOS PREVIOS:
- Python 3.8 o superior
- Docker y Docker Compose
- pip (gestor de paquetes de Python)

2. CREAR ENTORNO VIRTUAL:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
.\venv\Scripts\activate  # En Windows
```

3. INSTALAR DEPENDENCIAS:
```bash
pip install -r requirements.txt
```

4. INICIAR DOCKER:
```bash
cd Kafka/docker-kafka
docker-compose up -d
```

5. CREAR TOPICS DE KAFKA:
```bash
kafka-topics --create --topic prediction_requests --bootstrap-server localhost:29092 --if-not-exists
kafka-topics --create --topic prediction_results --bootstrap-server localhost:29092 --if-not-exists
```

6. INICIAR SERVICIOS (en terminales separadas):

Terminal 1 - API REST:
```bash
cd Api
python api_app.py
```

Terminal 2 - Servidor gRPC:
```bash 
cd GRP
python grp_app.py
```

Terminal 3 - Servicio Kafka:
```bash
cd Kafka
python app/prediction_service.py
```

7. EJECUTAR COMPARACIÓN:
```bash
python comparison_text.py
```

PUERTOS UTILIZADOS:
- REST API: 8000
- gRPC: 50051
- Kafka: 29092
- Zookeeper: 22181

PARA DETENER TODO:
1. Detener los scripts de Python con Ctrl+C en cada terminal
2. Detener Docker:
```bash
cd Kafka/docker-kafka
docker-compose down
```

VERIFICACIÓN DE SERVICIOS:
- REST API: http://localhost:8000/health
- gRPC: python GRP/test_client.py
- Kafka: docker-compose logs kafka

Si algo falla, asegúrate de que:
1. Docker esté corriendo
2. Todos los servicios estén iniciados
3. Los puertos no estén siendo usados por otras aplicaciones
# ModeloVinos

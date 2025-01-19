# Sistema de Comparación de Predicciones - ModeloVinos

Este proyecto implementa un sistema de comparación de predicciones utilizando Kafka, servicios REST y gRPC. Sigue los pasos descritos para configurar, ejecutar y detener el sistema.

---

## **Requisitos Previos**
Antes de comenzar, asegúrate de contar con lo siguiente instalado en tu sistema:

- **Python** 3.8 o superior
- **Docker** y **Docker Compose**
- **pip** (gestor de paquetes de Python)

---

## **Instalación y Configuración**

### 1. Crear un Entorno Virtual
Crea y activa un entorno virtual para aislar las dependencias del proyecto.

#### En Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

#### En Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Instalar Dependencias
Instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

### 3. Iniciar Docker
Inicia los servicios de Docker necesarios para Kafka y Zookeeper:

```bash
cd Kafka/docker-kafka
docker-compose up -d
```

### 4. Crear Topics en Kafka
Crea los topics necesarios para la comunicación entre servicios:

```bash
kafka-topics --create --topic prediction_requests --bootstrap-server localhost:29092 --if-not-exists
kafka-topics --create --topic prediction_results --bootstrap-server localhost:29092 --if-not-exists
```

---

## **Ejecutar el Sistema**

Abre terminales separadas para cada servicio y ejecuta los comandos correspondientes:

### Terminal 1 - API REST
```bash
cd Api
python api_app.py
```

### Terminal 2 - Servidor gRPC
```bash
cd GRP
python grp_app.py
```

### Terminal 3 - Servicio Kafka
```bash
cd Kafka
python app/prediction_service.py
```

### Terminal 4 - Comparación de Predicciones
Ejecuta el script para comparar las predicciones:

```bash
python comparison_text.py
```

---

## **Puertos Utilizados**

| Servicio        | Puerto |
|-----------------|--------|
| REST API        | 8000   |
| gRPC            | 50051  |
| Kafka           | 29092  |
| Zookeeper       | 22181  |

---

## **Detener el Sistema**

1. Detén los scripts de Python en cada terminal usando `Ctrl+C`.
2. Detén los servicios de Docker:

```bash
cd Kafka/docker-kafka
docker-compose down
```

---

## **Verificación de Servicios**

- **REST API**: Accede a [http://localhost:8000/health](http://localhost:8000/health) para verificar el estado del servicio.
- **gRPC**: Ejecuta el cliente de prueba:
  ```bash
  python GRP/test_client.py
  ```
- **Kafka**: Revisa los logs de Kafka:
  ```bash
  docker-compose logs kafka
  ```

---

## **Solución de Problemas**

Si encuentras problemas, verifica lo siguiente:

1. **Docker**: Asegúrate de que Docker esté en ejecución.
2. **Puertos**: Confirma que los puertos no estén siendo utilizados por otras aplicaciones.
3. **Servicios**: Asegúrate de que todos los servicios se hayan iniciado correctamente.

---

## **Opciones de Despliegue**

### Docker Individual
Cada servicio cuenta con su propio Dockerfile para construcción y despliegue individual:

#### API REST
```bash
cd Api
docker build -t wine-api .
docker run -p 8000:8000 wine-api
```

#### Servidor gRPC
```bash
cd GRP
docker build -t wine-grpc .
docker run -p 50051:50051 wine-grpc
```

#### Servicios Kafka
```bash
cd Kafka
docker build -t wine-kafka-service .
docker run --network kafka-network wine-kafka-service
```

### Docker Compose
Para desplegar todos los servicios juntos, utiliza el docker-compose principal:

```bash
docker-compose up -d
```

### Despliegue en Kubernetes (Minikube)
También puedes desplegar el sistema en un cluster local de Kubernetes usando Minikube:

1. **Inicia Minikube**
```bash
minikube start
```

2. **Aplica los manifiestos de Kubernetes**
```bash
# Desplegar API REST
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/api-service.yaml

# Desplegar gRPC
kubectl apply -f k8s/grpc-deployment.yaml
kubectl apply -f k8s/grpc-service.yaml

# Desplegar Kafka
kubectl apply -f k8s/kafka-deployment.yaml
kubectl apply -f k8s/kafka-service.yaml
```

3. **Verifica los despliegues**
```bash
kubectl get pods
kubectl get services
```

4. **Accede a los servicios**
```bash
# Obtén la URL de la API REST
minikube service wine-api --url

# Obtén la URL del servicio gRPC
minikube service wine-grpc --url
```

> **Nota**: Asegúrate de tener los archivos de configuración necesarios en el directorio `k8s/` de tu proyecto.

---

## **Estructura del Proyecto**

```plaintext
├── Api/
│   ├── api_app.py          # Servicio REST API
│   ├── Dockerfile         # Dockerfile para API REST
├── GRP/
│   ├── grp_app.py          # Servidor gRPC
│   ├── Dockerfile        # Dockerfile para gRPC
├── Kafka/
│   ├── app/
│   │   ├── prediction_service.py  # Servicio Kafka
│   ├── Dockerfile       # Dockerfile para servicio Kafka
│   ├── docker-kafka/       # Configuración de Docker para Kafka
├── k8s/                 # Manifiestos de Kubernetes
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   ├── grpc-deployment.yaml
│   ├── grpc-service.yaml
│   ├── kafka-deployment.yaml
│   ├── kafka-service.yaml
├── docker-compose.yml   # Compose para todo el sistema
├── comparison_text.py      # Comparador de predicciones
├── requirements.txt        # Dependencias del proyecto
```

---

## **Contribución**
Si deseas contribuir a este proyecto, abre un issue o crea un pull request en el repositorio correspondiente.

---

## **Licencia**
Este proyecto está licenciado bajo los términos de [MIT License](LICENSE).

--- 

¡Disfruta utilizando el sistema de comparación de predicciones! 🚀

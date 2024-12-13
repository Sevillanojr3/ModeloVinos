import requests
import json
from confluent_kafka import Producer, Consumer
import uuid
import time
import grpc
import numpy as np
from concurrent import futures

# Importamos el servicio gRPC (ajusta la ruta según tu configuración)
import sys
sys.path.append('..')
from GRP import wine_service_pb2
from GRP import wine_service_pb2_grpc

class PredictionComparison:
    def __init__(self):
        # Configuración para REST
        self.rest_url = "http://localhost:8000/predict"
        
        # Configuración para Kafka mejorada
        self.kafka_config = {
            'bootstrap.servers': 'localhost:29092',
            'client.id': 'comparison_client',
            'group.id': 'comparison_group',
            'auto.offset.reset': 'latest',
            'enable.auto.commit': True
        }
        
        # Configuración específica para productor
        self.producer_config = {
            'bootstrap.servers': 'localhost:29092',
            'client.id': 'comparison_producer',
            'message.timeout.ms': 5000,
            'delivery.timeout.ms': 10000
        }
        
        # Configuración específica para consumidor
        self.consumer_config = {
            'bootstrap.servers': 'localhost:29092',
            'group.id': 'comparison_consumer',
            'auto.offset.reset': 'latest',
            'enable.auto.commit': True,
            'session.timeout.ms': 10000,
            'heartbeat.interval.ms': 3000
        }
        
        self.kafka_request_topic = 'prediction_requests'
        self.kafka_response_topic = 'prediction_results'
        
        # Configuración para gRPC
        self.grpc_channel = grpc.insecure_channel('localhost:50051')
        self.grpc_stub = wine_service_pb2_grpc.WinePredictorStub(self.grpc_channel)

    def predict_rest(self, features):
        """Predicción usando REST API"""
        try:
            # Formato correcto según el error 422 recibido
            data = {
                "alcohol": features[0],
                "malic_acid": features[1],
                "ash": features[2],
                "alcalinity_of_ash": features[3],
                "magnesium": features[4],
                "total_phenols": features[5],
                "flavanoids": features[6],
                "nonflavanoid_phenols": features[7],
                "proanthocyanins": features[8],
                "color_intensity": features[9],
                "hue": features[10],
                "od280_od315": features[11],
                "proline": features[12]
            }
            
            response = requests.post(
                self.rest_url,
                json=data,
                timeout=5
            )
            
            if response.status_code != 200:
                return {
                    "method": "REST",
                    "status": "error",
                    "error": f"Error HTTP {response.status_code}: {response.text}"
                }
                
            result = response.json()
            return {
                "method": "REST",
                "status": "success",
                "prediction": result["prediction"],
                "time": response.elapsed.total_seconds()
            }
        except requests.Timeout:
            return {"method": "REST", "status": "error", "error": "Timeout en la conexión"}
        except requests.ConnectionError:
            return {"method": "REST", "status": "error", "error": "No se pudo conectar al servidor REST"}
        except Exception as e:
            return {"method": "REST", "status": "error", "error": str(e)}

    def predict_grpc(self, features):
        """Predicción usando gRPC"""
        try:
            start_time = time.time()
            request = wine_service_pb2.WineFeatures(
                alcohol=features[0],
                malic_acid=features[1],
                ash=features[2],
                alcalinity_of_ash=features[3],
                magnesium=features[4],
                total_phenols=features[5],
                flavanoids=features[6],
                nonflavanoid_phenols=features[7],
                proanthocyanins=features[8],
                color_intensity=features[9],
                hue=features[10],
                od280_od315=features[11],
                proline=features[12]
            )
            # Agregamos timeout de 5 segundos
            response = self.grpc_stub.PredictWine(request, timeout=5)
            elapsed_time = time.time() - start_time
            
            return {
                "method": "gRPC",
                "status": "success",
                "prediction": response.prediction,
                "time": elapsed_time
            }
        except grpc.RpcError as e:
            return {"method": "gRPC", "status": "error", "error": f"Error gRPC: {e.details()}"}
        except Exception as e:
            return {"method": "gRPC", "status": "error", "error": str(e)}

    def predict_kafka(self, features):
        """Predicción usando Kafka"""
        consumer = None
        producer = None
        try:
            start_time = time.time()
            
            # Crear productor
            producer = Producer(self.producer_config)
            
            # Crear consumidor con ID único
            consumer_config = {
                **self.consumer_config,
                'group.id': f'comparison_consumer_{uuid.uuid4()}'
            }
            consumer = Consumer(consumer_config)
            consumer.subscribe([self.kafka_response_topic])
            
            # Generar ID único para esta solicitud
            request_id = str(uuid.uuid4())
            
            # Preparar datos
            request_data = {
                'request_id': request_id,
                'features': features
            }
            
            # Enviar mensaje
            print(f"\nEnviando mensaje a Kafka con ID: {request_id}")
            producer.produce(
                self.kafka_request_topic,
                key=request_id.encode('utf-8'),
                value=json.dumps(request_data).encode('utf-8'),
                callback=lambda err, msg: print(f'Error al enviar: {err}' if err else f'Mensaje enviado correctamente a {msg.topic()}')
            )
            producer.flush(timeout=5)
            
            # Esperar respuesta
            print("Esperando respuesta de Kafka...")
            timeout_end = time.time() + 15
            while time.time() < timeout_end:
                msg = consumer.poll(1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    print(f"Error en consumer: {msg.error()}")
                    continue
                
                try:
                    response = json.loads(msg.value().decode('utf-8'))
                    print(f"Mensaje recibido: {response}")
                    
                    if response.get('request_id') == request_id:
                        return {
                            "method": "Kafka",
                            "status": "success",
                            "prediction": response["prediction"],
                            "time": time.time() - start_time
                        }
                except json.JSONDecodeError as e:
                    print(f"Error decodificando mensaje: {e}")
                except Exception as e:
                    print(f"Error procesando mensaje: {e}")
            
            raise Exception("Timeout esperando respuesta de Kafka")
            
        except Exception as e:
            return {"method": "Kafka", "status": "error", "error": str(e)}
        finally:
            # Cerrar conexiones
            if producer:
                producer.flush()
            if consumer:
                consumer.close()

    def run_comparison(self, features):
        """Ejecuta predicciones usando los tres métodos y compara resultados"""
        results = []
        
        # Verificar que los features sean válidos
        if len(features) != 13:
            print("Error: Se requieren exactamente 13 características")
            return
        
        # Convertir features a float
        try:
            features = [float(f) for f in features]
        except ValueError:
            print("Error: Todas las características deben ser números")
            return
        
        print("\nRealizando predicción con REST API...")
        rest_result = self.predict_rest(features)
        results.append(rest_result)
        print(f"REST completado: {rest_result['status']}")
        
        print("\nRealizando predicción con gRPC...")
        grpc_result = self.predict_grpc(features)
        results.append(grpc_result)
        print(f"gRPC completado: {grpc_result['status']}")
        
        print("\nRealizando predicción con Kafka...")
        kafka_result = self.predict_kafka(features)
        results.append(kafka_result)
        print(f"Kafka completado: {kafka_result['status']}")
        
        print("\n=== Resultados de la comparación ===")
        for result in results:
            print(f"\nMétodo: {result['method']}")
            print(f"Estado: {result['status']}")
            if result['status'] == 'success':
                print(f"Predicción: {result['prediction']}")
                print(f"Tiempo: {result['time']:.4f} segundos")
            else:
                print(f"Error: {result['error']}")

if __name__ == "__main__":
    # Crear instancia de la clase de comparación
    comparison = PredictionComparison()
    
    # Datos de ejemplo más realistas (13 características)
    sample_features = [
        13.20, # alcohol
        1.78,  # malic_acid
        2.14,  # ash
        11.2,  # alcalinity_of_ash
        100,   # magnesium
        2.65,  # total_phenols
        2.76,  # flavanoids
        0.26,  # nonflavanoid_phenols
        1.28,  # proanthocyanins
        4.38,  # color_intensity
        1.05,  # hue
        3.40,  # od280_od315
        1050   # proline
    ]
    
    # Ejecutar comparación
    print("Iniciando comparación de métodos de predicción...")
    comparison.run_comparison(sample_features)
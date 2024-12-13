from confluent_kafka import Producer, Consumer
import json
import uuid
import time

# Definimos los topics
REQUEST_TOPIC = 'prediction_requests'
RESPONSE_TOPIC = 'prediction_results'

# Configuración del productor
producer_conf = {
    'bootstrap.servers': 'localhost:29092'
}

# Configuración del consumidor
consumer_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'prediction_client',
    'auto.offset.reset': 'earliest'
}

producer = Producer(producer_conf)
consumer = Consumer(consumer_conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Error al enviar mensaje: {err}')
    else:
        print(f'Mensaje enviado a {msg.topic()}')

def send_prediction_request(features):
    request_id = str(uuid.uuid4())
    
    # Creamos la solicitud
    request_data = {
        'request_id': request_id,
        'features': features
    }
    
    # Enviamos la solicitud
    producer.produce(
        REQUEST_TOPIC,
        json.dumps(request_data).encode('utf-8'),
        callback=delivery_report
    )
    producer.flush()
    
    return request_id

if __name__ == "__main__":
    # Ejemplo de características (13 valores)
    sample_features = [0.0] * 13  # Ajusta estos valores según tus necesidades
    
    # Nos suscribimos al topic de respuestas
    consumer.subscribe([RESPONSE_TOPIC])
    
    # Enviamos la solicitud
    request_id = send_prediction_request(sample_features)
    print(f"Solicitud enviada con ID: {request_id}")
    
    # Esperamos la respuesta
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                continue
                
            response = json.loads(msg.value().decode('utf-8'))
            if response['request_id'] == request_id:
                print("Respuesta recibida:")
                print(f"Predicción: {response['prediction']}")
                print(f"Estado: {response['status']}")
                break
                
    except KeyboardInterrupt:
        print("Cerrando cliente...")
    finally:
        consumer.close() 
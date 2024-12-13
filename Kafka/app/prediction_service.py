from confluent_kafka import Consumer, Producer
import json
import joblib
import numpy as np

# Definimos los topics
REQUEST_TOPIC = 'prediction_requests'
RESPONSE_TOPIC = 'prediction_results'

# Cargamos el modelo usando joblib
MODEL_PATH = '/mnt/c/Users/jesus/Desarrollo/KAG-CLoud/random_forest_model.pkl'
model = joblib.load(MODEL_PATH)

# Configuración del consumidor
consumer_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'prediction_service',
    'auto.offset.reset': 'earliest'
}

# Configuración del productor
producer_conf = {
    'bootstrap.servers': 'localhost:29092'
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

# Nos suscribimos al topic
consumer.subscribe([REQUEST_TOPIC])

def delivery_report(err, msg):
    if err is not None:
        print(f'Error al enviar mensaje: {err}')
    else:
        print(f'Mensaje enviado a {msg.topic()}')

def process_prediction(data):
    try:
        # Verificamos que tengamos todas las características necesarias
        features = data.get('features', [])
        if len(features) != 13:
            raise ValueError(f"Se esperan 13 características, pero se recibieron {len(features)}")
        
        # Convertimos los datos a numpy array
        features = np.array(features).reshape(1, -1)
        
        # Realizamos la predicción
        prediction = int(model.predict(features)[0])  # Convertimos a int para serialización JSON
        
        return {
            'request_id': data['request_id'],
            'prediction': prediction,
            'status': 'success'
        }
    except Exception as e:
        return {
            'request_id': data.get('request_id', 'unknown'),
            'error': str(e),
            'status': 'error'
        }

print("Servicio de predicciones iniciado. Esperando mensajes...")

try:
    while True:
        msg = consumer.poll(1.0)
        
        if msg is None:
            continue
        if msg.error():
            print(f"Error del consumidor: {msg.error()}")
            continue
            
        try:
            # Decodificamos el mensaje
            value = json.loads(msg.value().decode('utf-8'))
            
            # Procesamos la predicción
            result = process_prediction(value)
            
            # Enviamos la respuesta
            producer.produce(
                RESPONSE_TOPIC,
                json.dumps(result).encode('utf-8'),
                callback=delivery_report
            )
            producer.flush()
            
        except Exception as e:
            print(f"Error procesando mensaje: {e}")

except KeyboardInterrupt:
    print("Cerrando servicio...")
finally:
    consumer.close()
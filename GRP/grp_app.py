import grpc
from concurrent import futures
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
import time

# Importar los stubs generados (después de compilar el .proto)
import wine_service_pb2
import wine_service_pb2_grpc

class WinePredictorServicer(wine_service_pb2_grpc.WinePredictorServicer):
    def __init__(self):
        # Cargar el modelo
        try:
            model_path = "/mnt/c/Users/jesus/Desarrollo/KAG-CLoud/random_forest_model.pkl"
            self.model = joblib.load(model_path)
            self.scaler = StandardScaler()
            print(f"Modelo cargado exitosamente desde: {model_path}")
            self.model_loaded = True
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            self.model_loaded = False
            self.model = None

    def PredictWine(self, request, context):
        if not self.model_loaded:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Modelo no cargado')
            return wine_service_pb2.WinePrediction()

        try:
            # Preparar los datos de entrada
            input_data = [[
                request.alcohol,
                request.malic_acid,
                request.ash,
                request.alcalinity_of_ash,
                request.magnesium,
                request.total_phenols,
                request.flavanoids,
                request.nonflavanoid_phenols,
                request.proanthocyanins,
                request.color_intensity,
                request.hue,
                request.od280_od315,
                request.proline
            ]]

            # Realizar la predicción
            prediction = self.model.predict(input_data)

            # Mapear las clases a descripciones
            wine_types = {
                1: "Tipo 1 - Vino de alta calidad",
                2: "Tipo 2 - Vino de calidad media",
                3: "Tipo 3 - Vino de calidad estándar"
            }

            return wine_service_pb2.WinePrediction(
                prediction=int(prediction[0]),
                wine_type=wine_types[int(prediction[0])]
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error en la predicción: {str(e)}')
            return wine_service_pb2.WinePrediction()

    def CheckHealth(self, request, context):
        status = "OK" if self.model_loaded else "ERROR"
        message = "Servicio funcionando correctamente" if self.model_loaded else "Modelo no cargado"
        
        return wine_service_pb2.HealthResponse(
            status=status,
            message=message,
            model_loaded=self.model_loaded
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wine_service_pb2_grpc.add_WinePredictorServicer_to_server(
        WinePredictorServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado en puerto 50051")
    try:
        while True:
            time.sleep(86400)  # Un día en segundos
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

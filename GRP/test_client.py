import grpc
import wine_service_pb2
import wine_service_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = wine_service_pb2_grpc.WinePredictorStub(channel)
        
        # Probar el health check
        health_response = stub.CheckHealth(wine_service_pb2.HealthRequest())
        print("Health Check:", health_response.status, "-", health_response.message)
        
        # Probar la predicción
        features = wine_service_pb2.WineFeatures(
            alcohol=12.72,
            malic_acid=1.81,
            ash=2.2,
            alcalinity_of_ash=18.8,
            magnesium=86.0,
            total_phenols=2.2,
            flavanoids=2.53,
            nonflavanoid_phenols=0.26,
            proanthocyanins=1.77,
            color_intensity=3.9,
            hue=1.16,
            od280_od315=3.14,
            proline=714.0
        )
        
        prediction = stub.PredictWine(features)
        print("Predicción:", prediction.prediction)
        print("Tipo de vino:", prediction.wine_type)

if __name__ == '__main__':
    run() 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import uvicorn
import os

app = FastAPI(title="API de Clasificación de Vinos")

# Variables globales para el modelo y el scaler
model = None
scaler = None

# Función para cargar el modelo
def load_model():
    global model, scaler
    try:
        # Intenta cargar desde diferentes rutas posibles
        possible_paths = [
            "random_forest_model.pkl",
            "../random_forest_model.pkl",
            "Api/random_forest_model.pkl"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"Cargando modelo desde: {path}")
                model = joblib.load(path)
                scaler = StandardScaler()
                return True
                
        raise FileNotFoundError("No se encontró el archivo del modelo en ninguna ubicación")
        
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        return False

# Cargar el modelo al iniciar la aplicación
if not load_model():
    print("ADVERTENCIA: El modelo no se pudo cargar. La API no funcionará correctamente.")

# Definir la estructura de datos de entrada
class WineFeatures(BaseModel):
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: float
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315: float
    proline: float

# Endpoint para la predicción
@app.post("/predict")
async def predict_wine(features: WineFeatures):
    try:
        # Convertir los datos de entrada en un array
        input_data = [[
            features.alcohol,
            features.malic_acid,
            features.ash,
            features.alcalinity_of_ash,
            features.magnesium,
            features.total_phenols,
            features.flavanoids,
            features.nonflavanoid_phenols,
            features.proanthocyanins,
            features.color_intensity,
            features.hue,
            features.od280_od315,
            features.proline
        ]]
        
        # Realizar la predicción
        prediction = model.predict(input_data)
        
        # Mapear las clases a descripciones más informativas
        wine_types = {
            1: "Tipo 1 - Vino de alta calidad",
            2: "Tipo 2 - Vino de calidad media",
            3: "Tipo 3 - Vino de calidad estándar"
        }
        
        return {
            "prediction": int(prediction[0]),
            "wine_type": wine_types[int(prediction[0])]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")

# Endpoint de salud
@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "El servicio está funcionando correctamente"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

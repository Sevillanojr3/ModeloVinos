import pickle
import numpy as np
import joblib

# Cargamos el modelo
MODEL_PATH = '/mnt/c/Users/jesus/Desarrollo/KAG-CLoud/random_forest_model.pkl'

print("Intentando cargar el modelo...")

# Intentar diferentes métodos de carga
try:
    # Intento 1: usando pickle
    print("Intentando con pickle...")
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    print(f"Error con pickle: {e}")
    try:
        # Intento 2: usando joblib
        print("\nIntentando con joblib...")
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Error con joblib: {e}")
        print("\nNo se pudo cargar el modelo con ningún método.")
        exit(1)

print("\n=== Información del Modelo ===")
print("Tipo de modelo:", type(model))

# Obtener información adicional
try:
    print("\nCaracterísticas del modelo:")
    if hasattr(model, 'n_features_in_'):
        print(f"Número de características esperadas: {model.n_features_in_}")
    if hasattr(model, 'feature_names_in_'):
        print(f"Nombres de las características: {model.feature_names_in_}")
    if hasattr(model, 'classes_'):
        print(f"Clases posibles: {model.classes_}")
    
    # Intentar una predicción de prueba
    if hasattr(model, 'n_features_in_'):
        print("\nIntentando predicción de prueba...")
        sample_input = np.zeros((1, model.n_features_in_))
        prediction = model.predict(sample_input)
        print("Predicción de ejemplo (con zeros):", prediction)
except Exception as e:
    print(f"\nError al obtener información adicional: {e}") 
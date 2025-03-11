from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
#import logging

#logging.basicConfig(level=logging.INFO)

# Charger le modèle RandomForest enregistré
model = joblib.load('../data/random_forest_model_plant_growth.pkl')

# Initialiser l'application FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Classe pour valider les données d'entrée
class PlantData(BaseModel):
    Sunlight_Hours: float
    Temperature: float
    Humidity: float
    Soil_Type: str  # les valeurs possibles sont "loam", "sandy", "clay"
    Water_Frequency: str  # les valeurs possibles sont "daily", "bi-weekly", "weekly"

# Fonction pour transformer les données d'entrée en format adapté au modèle
def transform_input(data):
    # Transformation des Soil_Type en colonnes binaires
    soil_type = {'loam': [0, 1, 0], 'sandy': [0, 0, 1], 'clay': [1, 0, 0]}
    soil = soil_type.get(data.Soil_Type, [0, 0, 0])  # Si l'entrée n'est pas valide, on renvoie [0, 0, 0]

    # Transformation de Water_Frequency en colonnes binaires
    water_freq = {'daily': [0, 1, 0], 'bi-weekly': [1, 0, 0], 'weekly': [0, 0, 1]}
    water = water_freq.get(data.Water_Frequency, [0, 0, 0])  # Si l'entrée n'est pas valide, on renvoie [0, 0, 0]

    # Créer le tableau d'entrées final avec les valeurs
    input_data = np.array([[
        data.Sunlight_Hours,
        data.Temperature,
        data.Humidity,
        soil[0],  # Soil_Type_clay
        soil[1],  # Soil_Type_loam
        soil[2],  # Soil_Type_sandy
        water[0],  # Water_Frequency_daily
        water[1],  # Water_Frequency_bi_weekly
        water[2]   # Water_Frequency_weekly
    ]])

    return input_data


@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API de la prédiction de Vie"}


# Route pour faire une prédiction
@app.post("/predict/")
async def predict(user_prefs: PlantData):
    # Vérification des données d'entrée
    if user_prefs.Soil_Type.lower() not in ["loam", "sandy", "clay"]:
        raise HTTPException(status_code=400, detail="Le type de sol doit être 'loam', 'sandy' ou 'clay'.")
    
    if user_prefs.Water_Frequency.lower() not in ["daily", "bi-weekly", "weekly"]:
        raise HTTPException(status_code=400, detail="La fréquence d'arrosage doit être 'daily', 'bi-weekly' ou 'weekly'.")
    
    #logging.info(f"Données reçues : {user_prefs}")
    
    # Transformer les données d'entrée
    input_data = transform_input(user_prefs)
    #logging.info(f"Données transformées : {input_data}")

    # Faire une prédiction avec le modèle
    prediction = model.predict(input_data)
    #logging.info(f"Prédiction faite : {prediction[0]}")

    # Retourner la prédiction
    return {"prediction": int(prediction[0])}
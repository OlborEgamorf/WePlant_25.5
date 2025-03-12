from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
from enum import Enum

#import logging

#logging.basicConfig(level=logging.INFO)

# Charger le modèle RandomForest enregistré
model_pred_croissance = joblib.load('../data/random_forest_model_plant_growth.pkl')

# Initialiser l'application FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définir les valeurs possibles pour Soil_Type et Water_Frequency avec Enum
class SoilType(str, Enum):
    limon = "limon"
    sable = "sable"
    argile = "argile"

class WaterFrequency(str, Enum):
    quotidien = "quotidien"
    semi_hebdomadaire = "semi-hebdomadaire"
    hebdomadaire = "hebdomadaire"

# Classe pour valider les données d'entrée
class PlantData(BaseModel):
    Sunlight_Hours: float # Intervalle possible : 0 - 12
    Temperature: float # Intervalle possible : 0 - 50
    Humidity: float # Intervalle possible : 0 - 100
    Soil_Type: str  # les valeurs possibles sont "limon", "sable", "argile"
    Water_Frequency: str  # les valeurs possibles sont "quotidien", "semi-hebdomadaire", "hebdomadaire"

# Fonction pour transformer les données d'entrée en format adapté au modèle
def transform_input(data):
    # Transformation des Soil_Type en colonnes binaires
    soil_type = {'limon': [0, 1, 0], 'sable': [0, 0, 1], 'argile': [1, 0, 0]}
    soil = soil_type.get(data.Soil_Type, [0, 0, 0])  # Si l'entrée n'est pas valide, on renvoie [0, 0, 0]

    # Transformation de Water_Frequency en colonnes binaires
    water_freq = {'quotidien': [0, 1, 0], 'semi-hebdomadaire': [1, 0, 0], 'hebdomadaire': [0, 0, 1]}
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
@app.post("/predict_vie/")
async def predict(
    Sunlight_Hours: float = Query(..., alias= "Heures d'ensoleillement"),  # entre 0 et 12 heures
    Temperature: float = Query(..., alias="Température"),  # entre 0 et 50°C
    Humidity: float = Query(..., alias="Humidité"),  # entre 0 et 100%
    Soil_Type: SoilType = Query(..., alias="Type de sol"),
    Water_Frequency: WaterFrequency = Query(..., alias="fréquence d'arrosage")
):
    # Transformer les données d'entrée
    input_data = transform_input(PlantData(
        Sunlight_Hours=Sunlight_Hours,
        Temperature=Temperature,
        Humidity=Humidity,
        Soil_Type=Soil_Type,
        Water_Frequency=Water_Frequency
    ))

    # Faire une prédiction avec le modèle
    prediction = model_pred_croissance.predict(input_data)
    
    # Si la prédiction = 1, la plante à une bonne croissance: 
    #   "🌱✨ La plante se développe sainement ! Les conditions environnementales et les soins apportés sont favorables à une croissance optimale"
    
    # Si la prédiction = 0, la plante à une mauvaise croissance:
    #   "😕 La croissance de la plante est insuffisante. Les conditions actuelles pourraient être optimisées en ajustant l’arrosage, l’exposition à la lumière ou le niveau d'humidité. "

    # Retourner la prédiction
    return {int(prediction[0])}
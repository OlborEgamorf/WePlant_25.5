import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from enum import Enum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définition des données sous forme de DataFrame
data = {
    "Sol": ["Sableux", "Limoneux", "Argileux"],
    "θopt_racinaires_profonds": [13.0, 20.5, 33.0],
    "θopt_racinaires_moyens": [14.0, 23.5, 38.0],
    "θopt_racinaires_superficiels": [5.9, 11.4, 22.9],
    "θwp": [5.0, 10.0, 20.0],
    "humidite_flet": [5.0, 12.0, 27.0],
    "humidite_racinaires_profonds": [20.8, 28.7, 39.6],
    "humidite_racinaires_moyens": [22.4, 32.9, 45.6],
    "humidite_racinaires_superficiels": [9.44, 15.96, 27.48]
}

# Définition des types de racines
types_racine_mapping = {
    "profondes": ["θopt_racinaires_profonds","humidite_racinaires_profonds"],
    "moyennes": ["θopt_racinaires_moyens","humidite_racinaires_moyens"],
    "superficielles": ["θopt_racinaires_superficiels", "humidite_racinaires_superficiels"]
}

# Densité apparente des sols (en g/cm³)
densite_apparente = {
    "Sableux": 1.6,
    "Limoneux": 1.3,
    "Argileux": 1.1
}

# Profondeur des pots en dm
profondeur_pots = {
    "M": 2,
    "L": 4,
    "XL": 6
}

diametre_pots = {
    "M": 2,
    "L": 4,
    "XL": 6
}

df = pd.DataFrame(data)

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API des paramètres des sols"}

@app.get("/parametres_sol/")
async def get_sol_parameters(
    sol: str = Query(..., description="Type de sol: Sableux, Limoneux, Argileux"),
    racine: str = Query(..., description="Type de racines: Profondes, Moyennes, Superficielles"),
    taille_pot: str = Query("M", description="Taille du pot: M, L, XL"),
    humidity: float = Query(..., description="Humidité actuelle du sol en %")
):
    """
    Récupère les paramètres d'un sol et d'un type de racine,
    puis calcule la Réserve Utile (RU) et indique si l'arrosage est nécessaire.
    """
    sol = sol.capitalize()
    racine = racine.lower()
    taille_pot = taille_pot.upper()

    # Vérification du type de sol
    if sol not in df["Sol"].values:
        raise HTTPException(status_code=404, detail="Type de sol non trouvé. Choisissez parmi: Sableux, Limoneux, Argileux")

    # Vérification du type de racine
    if racine not in types_racine_mapping:
        raise HTTPException(status_code=400, detail=f"Type de racine invalide. Choisissez parmi: {', '.join(types_racine_mapping.keys())}")

    # Vérification de la taille du pot
    if taille_pot not in profondeur_pots and taille_pot not in diametre_pots:
        raise HTTPException(status_code=400, detail=f"Taille de pot invalide. Choisissez parmi: {', '.join(profondeur_pots.keys())}")

    # Sélection des colonnes correspondant au type de racine
    filtered_df = df[df["Sol"] == sol][["Sol"] + types_racine_mapping[racine]]

    # Récupération de la valeur θopt correspondant à la racine choisie
    θopt = filtered_df[types_racine_mapping[racine][0]].values[0]  # Prend la valeur moyenne

    # Récupération de la valeur θflet correspondant au sol choisi
    index_sol = data["Sol"].index(sol)
    θflet = data["θwp"][index_sol]
    humidite_cible = filtered_df[types_racine_mapping[racine][1]].values[0]  # Prend la valeur moyenne
    humidite_flet = data["humidite_flet"][index_sol]

    # Récupération de la densité apparente du sol
    da = densite_apparente[sol]

    # Récupération de la profondeur du pot en dm
    z = profondeur_pots[taille_pot]
    d = diametre_pots[taille_pot]

    da_echantillon = da + humidity * da/100
    da_cible = da + humidite_cible * da/100
    da_flet = da + humidite_flet * da/100

    # Calcul de la Réserve Utile (RU en mm)
    RU_obs = (((θopt/100)*da_echantillon - (θflet/100)*da_flet)/da)*100  * da * z
    RU_cible = (((θopt/100)*da_cible - (θflet/100)*da_flet)/da)*100  * da * z
    # Vérification du besoin d’arrosage

    surface = 3.14 * d *100

    vol_eau_cm3_obs = RU_obs/10 * surface
    vol_eau_l_obs = vol_eau_cm3_obs/1000

    vol_eau_cm3_cible = RU_cible/10 * surface
    vol_eau_l_cible = vol_eau_cm3_cible/1000

    if vol_eau_l_obs < vol_eau_l_cible:
       volume_a_arroser = round(vol_eau_l_cible - vol_eau_l_obs,2)
    else:
       volume_a_arroser = 0
    
    besoin_arrosage = ("Il faut arroser de "+ str(volume_a_arroser) + " Litres") if volume_a_arroser>0 else "Pas besoin d'arroser"

    return {
        "sol": sol,
        "type_racine": racine,
        "taille_pot": taille_pot,
        "θopt": θopt,
        "θflet": θflet,
        "Humidité flet": humidite_flet,
        "RU_obs": round(RU_obs, 2),
        "RU_cible": round(RU_cible, 2),
        "densite_apparente": da,
        "profondeur_pot_dm": z,
        "humidite_mm": humidity,
        "volume_a_arroser": round(volume_a_arroser,2),
        "besoin_arrosage": besoin_arrosage
    }


#API Stress hydrique

def load_stress():
    model_stress = joblib.load("data/svm_plant_health.pkl")
    scaler_stress = joblib.load("data/scaler.pkl")
    return model_stress, scaler_stress

model_stress, scaler_stress = load_stress()

@app.get("/stress_hydrique")
def predict_health_status(
    soil_moisture: float = Query(..., description="Taux d'humidité du sol"),
    soil_temperature: float = Query(..., description="Température du sol"),
    nitrogen_level: float = Query(default=30.14, description="Niveau d'azote dans le sol"),
    phosphorus_level: float = Query(default=30.02, description="Niveau de phosphore dans le sol"),
    potassium_level: float = Query(default=30.49, description="Niveau de potassium dans le sol")
):
    try:
        # Transformer les données d'entrée
        input_data = np.array([[soil_moisture, soil_temperature, nitrogen_level, phosphorus_level, potassium_level]])
        input_data_scaled = scaler_stress.transform(input_data)
        
        # Prédire la classe et les probabilités
        prediction = model_stress.predict(input_data_scaled)
        prediction_proba = model_stress.predict_proba(input_data_scaled).tolist()[0]
        
        return {"prediction": int(prediction[0]), "prob0": prediction_proba[0],  "prob1": prediction_proba[1], "prob2": prediction_proba[2]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




# API Croissance Plante

# Charger le modèle RandomForest enregistré
model_pred_croissance = joblib.load('data/random_forest_model_plant_growth.pkl')

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

# Route pour faire une prédiction
@app.post("/predict_croissance/")
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
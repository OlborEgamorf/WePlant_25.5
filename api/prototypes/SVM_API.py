import pandas as pd
import numpy as np
import joblib
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Charger le modèle et le scaler
def load_stress():
    model_stress = joblib.load("data/svm_plant_health.pkl")
    scaler_stress = joblib.load("data/scaler.pkl")
    return model_stress, scaler_stress

model_stress, scaler_stress = load_stress()

# Définir l'API avec FastAPI
app = FastAPI()

# Middleware CORS (si nécessaire pour les requêtes cross-origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de prédiction de la santé des plantes"}

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


import openai
from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import os
import random
from dotenv import load_dotenv


openai.api_key =  ""
app = FastAPI()

# CORS pour autoriser les requêtes depuis n'importe quelle origine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définition du modèle des préférences utilisateur
class UserPreferences(BaseModel):
    SunNeeds: Optional[str] = Field(None, description="Besoins en soleil")
    WaterNeeds: Optional[str] = Field(None, description="Besoins en eau")
    Maintenance: Optional[str] = Field(None, description="Niveau de maintenance")
    Type_de_Sol: Optional[str] = Field(None, description="Type de sol")
    saison: Optional[str] = Field(None, description="Saison de croissance")
    plant_categories: Optional[str] = Field(None, description="Catégories de plantes")
    min_height_cm: Optional[float] = Field(None, description="Hauteur minimale en cm")
    max_height_cm: Optional[float] = Field(None, description="Hauteur maximale en cm")

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de recommandation de plantes"}

@app.post("/recommend_chat")
def get_recommendations(user_prefs: UserPreferences):

    response_gpt = generate_plant_recommendation(user_prefs)

    return {"recommendations": [response_gpt], "source": "GPT-4"}


# Fonction pour générer une recommandation avec GPT-4 si aucune plante ne correspond
def generate_plant_recommendation(user_prefs):
    prompt = f"""
    Je recherche une plante qui correspond aux critères suivants :
    - Exposition : {user_prefs.SunNeeds}
    - Type de sol : {user_prefs.Type_de_Sol}
    - Besoin en eau : {user_prefs.WaterNeeds}
    - Maintenance : {user_prefs.Maintenance}
    - Saison : {user_prefs.saison}
    - Catégorie : {user_prefs.plant_categories}
    - Taille : entre {user_prefs.min_height_cm} cm et {user_prefs.max_height_cm} cm

    Peux-tu recommander une plante adaptée en me donnant ces 4 informations sous ce format JSON :
    {{
        "Nom": "Nom de la plante",
        "Description": "Une description détaillée de la plante.",
        "Caractéristiques": "Les principales caractéristiques de la plante.",
        "ConseilsEntretien": "Les conseils pour entretenir cette plante."
    }}

    Réponds uniquement avec un JSON valide sans autre texte autour.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Tu es un expert en botanique et jardinage."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erreur lors de la requête OpenAI : {str(e)}"


# Charger les données CSV
csv_file = "./data/A_to_Z_Flowers_indicateurs.csv"
try:
    plant_data = pd.read_csv(csv_file)
except FileNotFoundError:
    raise FileNotFoundError(f"Le fichier {csv_file} n'a pas été trouvé. Vérifie le chemin.")


@app.post("/recommend")
def get_recommendations(user_prefs: UserPreferences):
    filtered_data = plant_data.copy()
    failed_criteria = [] 
    current_filters = {
        "SunNeeds": user_prefs.SunNeeds,
        "WaterNeeds": user_prefs.WaterNeeds,
        "Maintenance": user_prefs.Maintenance,
        "Type de Sol": user_prefs.Type_de_Sol,
        "saison": user_prefs.saison,
        "plant_categories": user_prefs.plant_categories,
    }
    
    for key, value in current_filters.items():
        if value and key in plant_data.columns:
            filtered_data = filtered_data[filtered_data[key].str.contains(value, na=False, case=False)]
    
    while filtered_data.empty and current_filters:
        key = random.choice(list(current_filters.keys()))
        value = current_filters[key]
        failed_criteria.append(key)
        del current_filters[key]
        
        filtered_data = plant_data.copy()
        for key, value in current_filters.items():
            if value and key in plant_data.columns:
                filtered_data = filtered_data[filtered_data[key].str.contains(value, na=False, case=False)]

    if user_prefs.min_height_cm is not None:
        filtered_data = filtered_data[filtered_data["min_height_cm"] >= user_prefs.min_height_cm]
    if user_prefs.max_height_cm is not None:
        filtered_data = filtered_data[filtered_data["max_height_cm"] <= user_prefs.max_height_cm]
    
    success = True
    recommendations = filtered_data["Name"].head(5).tolist()
    if not recommendations:
        recommendations = plant_data["Name"].head(5).tolist()
        success = False
    
    return {"recommendations": recommendations, "success":success, "failed_criteria": failed_criteria, "hasFailed":len(failed_criteria) != 0} 

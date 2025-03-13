from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import random
from fastapi import HTTPException, WebSocketException
import numpy as np

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SELECTED_COLUMNS = [
    "Name", 
    "SunNeeds", 
    "WaterNeeds", 
    "Maintenance", 
    "Type de Sol", 
    "saison", 
    "plant_categories", 
    "min_height_cm", 
    "max_height_cm"
]

def df_to_dict(df: pd.DataFrame) -> list:
    """Convertit un DataFrame en liste de dictionnaires compatibles JSON avec colonnes sélectionnées"""
    return [
        {col: (str(value) if isinstance(value, (list, dict)) else value) 
         for col, value in record.items() if col in SELECTED_COLUMNS}
        for record in df.to_dict(orient='records')
    ]

try:
    csv_file = "../data/A_to_Z_Flowers_indicateurs.csv"
    plant_data = pd.read_csv(csv_file).fillna(np.nan).replace([np.nan], [None])
except Exception as e:
    raise RuntimeError(f"Erreur de chargement du CSV: {str(e)}")


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




@app.post("/recommend")
async def get_recommendations(user_prefs: UserPreferences):
    try:
        filtered_data = plant_data.copy()
        failed_criteria = []
        
        # Configuration des filtres
        filters = {
            "SunNeeds": user_prefs.SunNeeds,
            "WaterNeeds": user_prefs.WaterNeeds,
            "Maintenance": user_prefs.Maintenance,
            "Type de Sol": user_prefs.Type_de_Sol,
            "saison": user_prefs.saison,
            "plant_categories": user_prefs.plant_categories
        }

        # Application des filtres catégoriels
        for key, value in filters.items():
            if value and key in filtered_data.columns:
                filtered_data = filtered_data[
                    filtered_data[key].str.contains(value, case=False, na=False)
                ]

        # Relâchement progressif des filtres si nécessaire
        while filtered_data.empty and filters:
            removed_filter = random.choice(list(filters.keys()))
            failed_criteria.append(removed_filter)
            del filters[removed_filter]
            
            filtered_data = plant_data.copy()
            for key, value in filters.items():
                if value and key in filtered_data.columns:
                    filtered_data = filtered_data[
                        filtered_data[key].str.contains(value, case=False, na=False)
                    ]

        # Filtrage numérique pour la hauteur
        if user_prefs.min_height_cm is not None:
            filtered_data = filtered_data[filtered_data["min_height_cm"] >= user_prefs.min_height_cm]
        if user_prefs.max_height_cm is not None:
            filtered_data = filtered_data[filtered_data["max_height_cm"] <= user_prefs.max_height_cm]

        # Préparation des résultats
        result_count = min(5, len(filtered_data))
        final_data = filtered_data[SELECTED_COLUMNS].head(result_count) if not filtered_data.empty else plant_data[SELECTED_COLUMNS].head(5)
        
        return {
            "recommendations": df_to_dict(final_data),
            "success": not filtered_data.empty,
            "failed_criteria": failed_criteria,
            "hasFailed": len(failed_criteria) > 0
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne: {str(e)}"
        )
from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


csv_file = "../data/A_to_Z_Flowers_indicateurs.csv"  
plant_data = pd.read_csv(csv_file)

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
def get_recommendations(user_prefs: UserPreferences):
    filtered_data = plant_data.copy()
    failed_criteria = []
    
    filters = {
        "SunNeeds": user_prefs.SunNeeds,
        "WaterNeeds": user_prefs.WaterNeeds,
        "Maintenance": user_prefs.Maintenance,
        "Type de Sol": user_prefs.Type_de_Sol,
        "saison": user_prefs.saison,
        "plant_categories": user_prefs.plant_categories,
    }
    
    for key, value in filters.items():
        if value and key in plant_data.columns:
            if not plant_data[key].str.contains(value, na=False, case=False).any():
                failed_criteria.append(key)
            else:
                filtered_data = filtered_data[filtered_data[key].str.contains(value, na=False, case=False)]
    
    if user_prefs.min_height_cm is not None:
        filtered_data = filtered_data[filtered_data["min_height_cm"] >= user_prefs.min_height_cm]
    if user_prefs.max_height_cm is not None:
        filtered_data = filtered_data[filtered_data["max_height_cm"] <= user_prefs.max_height_cm]
    
    recommendations = filtered_data["Name"].head(5).tolist()
    
    if not recommendations:
        return {
            "message": "Aucune correspondance exacte trouvée.",
            "failed_criteria": failed_criteria,
            "recommendations": plant_data["Name"].head(5).tolist()
        }
    
    return {"recommendations": recommendations}
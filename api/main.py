import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

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
    "θopt_racinaires_profonds_min": [12.5, 20.0, 32.5],
    "θopt_racinaires_profonds_max": [13.5, 21.0, 33.5],
    "θopt_racinaires_moyens": [14.0, 23.5, 38.0],
    "θopt_racinaires_superficiels": [5.9, 11.4, 22.9],
    "θopt_racinaires_superficiels_min": [5.0, 10.5, 22.0],
    "θopt_racinaires_superficiels_max": [6.8, 12.3, 23.8]
}

# Définition des types de racine disponibles
types_racine_mapping = {
    "profonds": ["θopt_racinaires_profonds", "θopt_racinaires_profonds_min", "θopt_racinaires_profonds_max"],
    "moyens": ["θopt_racinaires_moyens"],
    "superficiels": ["θopt_racinaires_superficiels", "θopt_racinaires_superficiels_min", "θopt_racinaires_superficiels_max"]
}

df = pd.DataFrame(data)

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API des paramètres des sols"}

@app.get("/parametres_sol/")
async def get_sol_parameters(
    sol: str = Query(..., description="Type de sol: Sableux, Limoneux, Argileux"),
    racine: str = Query(..., description="Type de racine: Profonds, Moyens, Superficiels")
):
    """
    Récupère les paramètres spécifiques d'un sol et d'un type de racine.
    Exemple : /parametres_sol/?sol=Sableux&racine=profonds
    """
    sol = sol.capitalize()
    racine = racine.lower()

    # Vérification du type de sol
    if sol not in df["Sol"].values:
        raise HTTPException(status_code=404, detail="Type de sol non trouvé. Choisissez parmi: Sableux, Limoneux, Argileux")

    # Vérification du type de racine
    if racine not in types_racine_mapping:
        raise HTTPException(status_code=400, detail=f"Type de racine invalide. Choisissez parmi: {', '.join(types_racine_mapping.keys())}")

    # Sélection des colonnes correspondant au type de racine
    filtered_df = df[df["Sol"] == sol][["Sol"] + types_racine_mapping[racine]]

    # Conversion en dictionnaire
    params = filtered_df.to_dict(orient="records")[0]
    
    return {"sol": sol, "type_racine": racine, "parametres": params}

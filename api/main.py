import numpy as np

from typing import Annotated
from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# documentation de fastapi : https://fastapi.tiangolo.com/learn/
# documentation de NOTRE API : http://127.0.0.1:8000/docs
# la documentation permet de tester les routes facilement !


# lancer l'API : fastapi dev ./api/main.py

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test(nombre:int=2, texte:str="ttt"):
    # :int spécifie un entier, =2 donne la valeur par défaut du paramètre nombre
    # :str spécifie une chaine de caractère, ="ttt" donne la valeur par défaut du paramètre texte
    # donner le type fait que si un élément du mauvais type est entré par l'utilisateur, l'API bloquera la requete
    # exemple de requete ici : http://127.0.0.1:8000/test?nombre=400&texte=eeerreereereee
    
    # le retour est un dictionnaire, pour le contenu tu mets ce que tu veux !
    return {"texte":texte, "nombre": nombre}


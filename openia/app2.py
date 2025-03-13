import streamlit as st
import pandas as pd
import openai

# Charger les données
df = pd.read_csv("../data/A_to_Z_Flowers_indicateurs.csv")

openai.api_key = ""
# Interface utilisateur Streamlit
st.title("🌿 Recommandation de Plantes")

# Sélection des critères
exposition = st.selectbox("Exposition ☀️", ["Ombre", "Mi-ombre", "Plein soleil"])
type_sol = st.selectbox("Type de sol 🏺", ["Argile", "Limon", "Sable"])
besoin_eau = st.selectbox("Besoin en eau 💧", ["Faible", "Moyen", "Élevé"])
maintenance = st.selectbox("Maintenance 🛠️", ["Faible", "Moyenne", "Difficile"])
saison = st.selectbox("Saison 🍂", ["Printemps", "Été", "Automne", "Hiver"])
categorie = st.selectbox("Catégorie 🌱", ["Grimpantes", "Vivaces", "Arbustes", "Fleurs"])
taille = st.slider("Taille (en cm) 📏", 30, 300, (50, 150))

# Fonction pour générer la recommandation
def recommander_plante(exposition, type_sol, besoin_eau, maintenance, saison, categorie, taille_min, taille_max):
    prompt = f"""
    Je recherche une plante qui correspond aux critères suivants :
    - Exposition : {exposition}
    - Type de sol : {type_sol}
    - Besoin en eau : {besoin_eau}
    - Maintenance : {maintenance}
    - Saison : {saison}
    - Catégorie : {categorie}
    - Taille : entre {taille_min} cm et {taille_max} cm

    Peux-tu recommander une plante adaptée avec une description détaillée, ses caractéristiques et des conseils d’entretien ?
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Tu es un expert en botanique et jardinage."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erreur lors de la requête OpenAI : {str(e)}"

# Bouton pour générer la recommandation
if st.button("🌱 Trouver une plante adaptée"):
    plante_recommandee = recommander_plante(exposition, type_sol, besoin_eau, maintenance, saison, categorie, taille[0], taille[1])
    st.subheader("🌿 Plante recommandée")
    st.write(plante_recommandee)

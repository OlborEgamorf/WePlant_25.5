import streamlit as st
import pandas as pd
import openai

# Charger les données
df = pd.read_csv("../data/A_to_Z_Flowers_indicateurs.csv")

# Clé API OpenAI (⚠️ NE PAS LA METTRE EN CLAIR, utiliser une variable d'environnement)
openai.api_key = ""

def chatgpt_recommendation(prompt):
    """
    Envoie le prompt à ChatGPT pour obtenir une description de la plante idéale.
    Utilise la nouvelle syntaxe de l'API OpenAI.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un expert en botanique et tu aides à recommander des plantes."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]  # Extraction de la réponse

def filtrer_plante(reponse_ai, df):
    """
    Utilise la description générée par ChatGPT pour filtrer les plantes dans notre dataset avec un système de score.
    """
    filtered_df = df.copy()
    
    # Définition des mots-clés pour les critères
    criteres = {
        "lumière": {
            "ombre": ["Ombre"],
            "mi-ombre": ["Mi-ombre"],
            "soleil": ["Plein soleil"]
        },
        "eau": {
            "peu d'eau": ["Faible"],
            "moyenne": ["Moyenne"],
            "beaucoup d'eau": ["Elevée"]
        },
        "maintenance": {
            "peu d’entretien": ["Faible"],
            "entretien moyen": ["Moyen"],
            "entretien élevé": ["Difficile"]
        }
    }
    
    # Création d'un score pour classer les résultats
    filtered_df["score"] = 0
    
    # 🔍 Analyse des critères mentionnés dans la réponse de ChatGPT
    for critere, valeurs in criteres.items():
        for mot_cle, valeurs_associees in valeurs.items():
            if mot_cle in reponse_ai.lower():
                for valeur in valeurs_associees:
                    if critere == "lumière":
                        filtered_df.loc[filtered_df["SunNeeds"].str.contains(valeur, na=False), "score"] += 1
                    elif critere == "eau":
                        filtered_df.loc[filtered_df["WaterNeeds"].str.contains(valeur, na=False), "score"] += 1
                    elif critere == "entretien":
                        filtered_df.loc[filtered_df["Maintenance"].str.contains(valeur, na=False), "score"] += 1
    
    # 🌷 Ajout de la saison si mentionnée dans la réponse
    for saison in ["Printemps", "Été", "Automne", "Hiver"]:
        if saison.lower() in reponse_ai.lower():
            filtered_df.loc[filtered_df["saison"].str.contains(saison, na=False), "score"] += 1

    # 🌱 Ajout du type de sol si mentionné
    for sol in ["Argile", "Limon", "Sable"]:
        if sol.lower() in reponse_ai.lower():
            filtered_df.loc[filtered_df["Type de Sol"].str.contains(sol, na=False), "score"] += 1

    # 🎯 Trier les plantes par score décroissant et retourner les meilleures suggestions
    filtered_df = filtered_df.sort_values(by="score", ascending=False)
    result = filtered_df[["Name", "Desc", "SunNeeds", "WaterNeeds", "Maintenance", "saison", "Type de Sol", "score"]].head(3)
    
    return result if not result.empty else "❌ Aucune plante ne correspond aux critères."

st.title("🌿 Recommandation de Plantes")

# Champ de texte pour le prompt utilisateur
prompt_utilisateur = st.text_input("Décrivez votre plante idéale :")

if st.button("Rechercher"):
    if prompt_utilisateur:
        # Étape 1 : Obtenir la description de la plante idéale via ChatGPT
        try:
            reponse_ai = chatgpt_recommendation(prompt_utilisateur)
            st.write(f"🤖 **Plante idéale selon ChatGPT :** {reponse_ai}")

            # Étape 2 : Filtrer dans les données
            plantes_recommandees = filtrer_plante(reponse_ai, df)

            # Afficher les résultats
            if not plantes_recommandees.empty:
                st.write("🌱 **Plantes recommandées :**")
                st.dataframe(plantes_recommandees)
            else:
                st.write("❌ Aucune plante ne correspond aux critères.")
        except openai.error.RateLimitError:
            st.write("⚠️ **Erreur : Tu as dépassé ton quota d'utilisation. Vérifie ton abonnement OpenAI !**")
        except Exception as e:
            st.write(f"❌ **Erreur lors de l'appel à l'API OpenAI :** {e}")

    else:
        st.write("❗ Veuillez entrer une description.")

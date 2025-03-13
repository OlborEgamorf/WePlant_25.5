import pandas as pd
import numpy as np
import FATS
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import classification_report

# Chargement des données
df = pd.read_csv("data/plant_health_data.csv")

# Conversion de la colonne Timestamp en datetime et tri des données
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values(by=["Plant_ID", "Timestamp"])

# Sélection des variables explicatives et de la variable cible
features = ["Soil_Moisture", "Soil_Temperature", "Nitrogen_Level", "Phosphorus_Level", "Potassium_Level"]
target = "Plant_Health_Status"

# Encodage ordinal de la variable cible (qualitative ordinale)
encoder = OrdinalEncoder()
df[target] = encoder.fit_transform(df[[target]])

# Fonction pour normaliser une série
def normalize_series(series):
    return (series - np.mean(series)) / np.std(series) if np.std(series) != 0 else series

# Dictionnaire pour stocker les caractéristiques extraites
extracted_features = {}

# Extraction des caractéristiques FATS pour chaque plante et chaque variable
for plant_id in df["Plant_ID"].unique():
    plant_data = df[df["Plant_ID"] == plant_id]

    # Normalisation des variables explicatives
    normalized_data = {feature: normalize_series(plant_data[feature].values) for feature in features}

    # Extraction des caractéristiques pour chaque variable explicative
    for feature, values in normalized_data.items():
        # Création de l'objet TimeSeries
        ts = FATS.TimeSeries(values, plant_data["Timestamp"].values)
        
        # Liste des caractéristiques à extraire
        feature_list = ["Mean", "Std", "Skewness", "Kurtosis", "Amplitude", "PercentDifferenceFluxPercentile"]
        
        # Création de l'objet FeatureSpace
        fs = FATS.FeatureSpace(feature_list=feature_list)
        
        # Calcul des caractéristiques
        f_values = fs.calculate_features(ts)
        
        # Stockage des caractéristiques
        extracted_features[(plant_id, feature)] = f_values.result(method="dict")

# Conversion du dictionnaire de caractéristiques en DataFrame
features_df = pd.DataFrame.from_dict(extracted_features, orient='index')

# Réorganisation des données pour correspondre aux Plant_ID
features_df.index = pd.MultiIndex.from_tuples(features_df.index, names=["Plant_ID", "Feature"])
features_df = features_df.unstack(level=1)
features_df.columns = ["_".join(col).strip() for col in features_df.columns.values]  # Flatten column names

# Séparation des jeux de données (8 plantes pour l'entraînement, 2 pour le test)
plant_ids = df["Plant_ID"].unique()
train_plants = plant_ids[:8]
test_plants = plant_ids[8:]

X_train = features_df.loc[train_plants]
X_test = features_df.loc[test_plants]

# Extraction des étiquettes cibles (valeur finale par plante)
y_train = df[df["Plant_ID"].isin(train_plants)].groupby("Plant_ID")[target].last()
y_test = df[df["Plant_ID"].isin(test_plants)].groupby("Plant_ID")[target].last()

# Entraînement d'un modèle RandomForest pour la classification
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Prédictions et évaluation
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=encoder.categories_[0]))

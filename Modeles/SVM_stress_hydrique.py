import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, accuracy_score

# Charger les données
data = pd.read_csv("data/plant_health_data.csv")

# Sélectionner les variables explicatives et la cible
features = ["Soil_Moisture", "Soil_Temperature", "Nitrogen_Level", "Phosphorus_Level", "Potassium_Level"]
target = "Plant_Health_Status"

X = data[features]
y = data[target]

# Encoder la variable cible
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Récupérer les noms des classes
class_labels = label_encoder.classes_

# Séparer les données en train et test
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

# Normaliser les données
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Optimisation des hyperparamètres
param_grid = {'estimator__C': [0.1, 1, 10], 'estimator__kernel': ['linear', 'rbf', 'poly']}
svm_model = OneVsRestClassifier(SVC(probability=True, random_state=42))
grid_search = GridSearchCV(svm_model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Meilleur modèle
best_model = grid_search.best_estimator_

# Enregistrer le modèle et le scaler
joblib.dump(best_model, "data/svm_plant_health.pkl")
joblib.dump(scaler, "data/scaler.pkl")

# Prédictions
# Prédictions (avec inversion des labels pour obtenir les classes qualitatives)
y_pred = best_model.predict(X_test)
y_pred_classes = label_encoder.inverse_transform(y_pred)  # Inverser les labels prédits

y_prob = best_model.predict_proba(X_test)
y_prob_classes = label_encoder.inverse_transform(np.argmax(y_prob, axis=1))  # Inverser les classes avec la probabilité la plus élevée

# Évaluation du modèle
print("Best Parameters:", grid_search.best_params_)
print(classification_report(y_test, y_pred, target_names=class_labels))

# Calcul de l'AUC
auc_score = roc_auc_score(y_test, y_prob, multi_class='ovr')
print("AUC Score:", auc_score)

# Calcul de l'AIC et du BIC
n = X_test.shape[0]  # Nombre d'échantillons
k = X_test.shape[1]  # Nombre de variables explicatives
log_likelihood = -np.sum(np.log(y_prob[np.arange(len(y_test)), y_test] + 1e-9))
AIC = 2 * k - 2 * log_likelihood
BIC = k * np.log(n) - 2 * log_likelihood
print(f"AIC: {AIC}, BIC: {BIC}")

# Visualisation des résultats avec les classes qualitatives
plt.figure(figsize=(10, 6))
sns.heatmap(pd.crosstab(pd.Series(label_encoder.inverse_transform(y_test), name='Actual'), 
                        pd.Series(y_pred_classes, name='Predicted')), 
            annot=True, fmt='d', cmap='Blues')
plt.title("Matrice de Confusion")
plt.show()

# Tracer les courbes ROC pour chaque classe
plt.figure(figsize=(10, 6))
for i, class_name in enumerate(class_labels):
    fpr, tpr, _ = roc_curve(y_test == i, y_prob[:, i])
    plt.plot(fpr, tpr, label=f'Classe {class_name}')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('Taux de faux positifs')
plt.ylabel('Taux de vrais positifs')
plt.title('Courbes ROC')
plt.legend()
plt.show()


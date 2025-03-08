# data - Données 

## Contenu du dossier 

Tous les fichiers CSV comportant nos données se trouvent ici. Merci de bien mettre à jour ce Markdown quand un fichier est ajouté, modifié ou supprimé.

## Détail de chaque fichier 

- A_to_Z_Flowers_cleaned - 223 lignes
  - détaille 223 espèces de fleurs avec description, couleurs, saison de floraison, taille et besoins
  - beaucoup de texte, modalités claires ou non
  - source : https://www.kaggle.com/datasets/kkhandekar/a-to-z-flowers-features-images/data
  - traité : descriptions qui étaient en HTML, colonne RelatedFlowers supprimée car chaque entrée avait la même valeur
- plant_growth_data
  - conçu pour faire de la classification binaire
  - plusieurs paramètres : type de sol, temps au soleil, fréquence d'arrosage, ... et si la plante arrive à pousser (0 ou 1)
  - assez clair, mais les plantes sont quelconques, seul l'environnement change
  - source : https://www.kaggle.com/datasets/gorororororo23/plant-growth-data-classification
- plant_growth_hydroponic_and_soil
  - ???
  - source : https://www.kaggle.com/datasets/abtabm/plant-growthhydroponics-and-soil-compound-dataset
- plant_health_data
  - relevé de la santé d'une plante dans le temps, avec beaucoup de caractéristiques
  - 3 niveaux de santé : High Stress (article de la mort), Moderate Stress (déshydratée), Healthy (en bonne santé)
  - pourrait permettre de la classification, mais la plante est inconnue et unique
  - source : https://www.kaggle.com/datasets/ziya07/plant-health-data
- plant_health_monitor_data
  - même source que le jeu de données précédent
  - pas dans le temps, mais pour différentes plantes non identifiées
  - score de santé de 0 à 100
  - source : https://www.kaggle.com/datasets/ziya07/plant-health-monitoring

## Historique fichiers modifiés

## Historiques données supprimées
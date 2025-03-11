# WePlant_25.5

Marathon du web M1 MIASHS UMPV 2025. 

## Composition du groupe

- Justin Emanuel
- Noah Guyon
- Gautier Meyrieux
- Aya Mohamedatni
- Cassandra Sénécaille
- Lucas Triozon

## Lancement site web

Nécessite d'avoir NodeJS 20 ou version supérieure pour fonctionner.

Le site est codé avec Svelte, Sveltekit et TypeScript.

Lors de la première utilisation, installer tous les packages avec npm :

```bash
npm install
```

Ensuite, lancer le site :

```bash
npm run dev
```

Bibliothèque des composants pour importer de nouveaux éléments : https://www.shadcn-svelte.com/

## Règles de contributions

Ce projet étant court et à 6, il n'y a pas de temps à perdre dans la gestion de Git et de la lisibilité du code. Voici les règles à respecter quand vous écrivez du code et que vous le publiez ici :

- Tous les fichiers doivent être bien compartimentés
  - aucun fichier dans le dossier racine, sauf ceux liés à l'environnement (`requirements.txt`, `.env`, ...)
  - les données dans `data/`
  - les notebooks Python d'exploration dans `notebooks/`
  - si une catégorie n'existe pas encore, ajouter un dossier et mettre un nom cohérent !

- Bien coder en Python
  - Chaque variable doit être claire et explicite, quitte à ce qu'elle soit trop longue. Exemple : `df1`, `df2`, `df3` pour désigner des DataFrame différents n'est pas acceptable. Privilégier dans ce cas là plutôt des noms en lien avec les données, ou le nom du fichier importé. Si on ne peut pas comprendre une variable par son nom, c'est qu'il faut la changer.
  - Les notebooks `.ipynb` doivent être rangés et classés dans des sections / sous-sections pour un maximum de lisibilité. Pas de bloc de code laissé dans la nature sans explication. Privilégier des titres.
  - Si des choses (notamment en algorithmique) ne sont pas claires à la lecture du code, ajouter des commentaires. Lignes par lignes s'il le faut.
  - Garder des notebooks à thème. Un notebook axé sur la data viz ne doit pas comporter du traitement ou du filtrage.
  - Ne rien publier qui ne fonctionne pas. Il faut pouvoir run les notebook intégralement sans qu'il y est de problèmes.
  - Chaque nouveau package ajouté par pip doit être mis à jour aussi dans `requirements.txt`
  
- Bien utiliser Git
  - Chaque commit doit être nommé de manière efficace. Pas de "Bug fix", "Nouvelle feature"... Expliquez ce qui a été changé de manière claire et non consise s'il le faut.
  - Pensez aussi à utiliser l'espace de commentaire pour ajouter des notes supplémentaires si besoin.
  - Servez vous des branches ! La branche `main` est reservée au contenu validé qui fonctionne parfaitement.
  - Mettre à jour les `README.md` dans tout le repo quand c'est nécessaire.

De manière globale, votre mère doit pouvoir comprendre ce qui se passe dans les fichiers et sur le Git. L'objectif est d'éviter des confusions et des appels non nécessaires.
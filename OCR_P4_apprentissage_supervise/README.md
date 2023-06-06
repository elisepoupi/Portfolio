# Objectifs du projet
La ville de Seattle a mené des relevés minutieux sur la consommation électrique des bâtiments pendant une année. Les données sont disponible ici sur le [site de Seattle](https://data.seattle.gov/dataset/2016-Building-Energy-Benchmarking/2bpz-gwpy).  

Ces relevés sont coûteux et il nous faut construire un modèle de prédiction pour déduire à l'avenir les données de consommations et d'émissions de gaz à effet de serre uniquement à partir des données structurelles des bâtiments.  

Nous devons également évaluer l'intérêt du score EnergyStar dans la modélisation.  

# Contraintes
- analyse exploratoire
- optimisation des hyperparamètres avec la validation croisée
- test de différents modèles de prédiction
- test de différentes transformations des variables (normalisation, passage au log...)
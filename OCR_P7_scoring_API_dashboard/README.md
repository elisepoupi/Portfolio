# Objectifs du projet
Pour ce projet, les objectifs étaient nombreux :
- À partir de ce [jeu de données](https://www.kaggle.com/c/home-credit-default-risk/data), réaliser un modèle de scoring pour calculer la probabilité qu'un client rembourse son crédit.
- Construire un dashboard interactif à destination des gestionnaires de la relation client permettant d'interpréter les prédictions faites par le modèle, et d’améliorer la connaissance client des chargés de relation client.
- Mettre en production le modèle de scoring de prédiction à l’aide d’une API, ainsi que le dashboard interactif qui appelle l’API pour les prédictions.  
  
# Contraintes
- pour la modélisation :
  - utilisation de la Cross-Validation ou GridSearchCV
  - prise en compte du déséquilibre des classes
  - création d'un score métier pour comparaison et évaluation des modèles, pour l'optimisation des hyperparamètres
  - étude de l'interprétabilité globale et locale du modèle
- pour le dashboard :
  - visualiser le score et son interprétation de façon intelligible pour une personne non experte en data
  - visualiser les informations descriptives relatives à un client avec un système de filtre
  - comparer les informations descriptives du client à l'ensemble des autres clients ou à un groupe de clients similaires
- gestion du cycle de vie du modèle avec l'utilisation de MLFlow, Git, Github, Github Actions et Pytest
- analyse du DataDrift avec Evidently
- déploiement du dashboard et de l'API sur une plateforme Cloud
- réalisation d'une note technique sur la démarche d'élaboration du modèle
- exécution de tests unitaires avec Pytest ou Unittest
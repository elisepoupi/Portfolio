Introduction :

    Le dashboard permet au chargé de relation client de visualiser les données relatives à une demande de prêt avec son client et de classifier la demande selon une probabilité de remboursement du prêt. Il permet également de modifier ces données et de relancer une prédiction à partir des données modifiées.

    Pour le test, utiliser des noms de personnage de Game of Thrones. 
    Par exemple : Robert, Ellaria, Samwell, Brandon...

Endpoints : 

    GET /
    POST /donnees/
    POST /score/
    POST /score_no_modif/


Base URL :

    https://epoupi-pret-a-depenser.herokuapp.com/


Authentication :

    aucune

Paramètres : 
    
    Les paramètres sont envoyés automatiquement par l'application. Il n'est pas possible de les écrire manuellement.

Architecture du dossier :
    - static/
	|---> fichiers .csv des données nécessaires à l'affichage des données, à l'envoi des données à l'API de prédiction et à la classification du prêt
	|---> images diverses utilisées dans l'application
	|---> feuilles de style .css
    - templates/
	|---> pages .html 

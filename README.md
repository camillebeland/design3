#Projet de Design III
## Pirates des Caraïbes
### Description Sommaire
Le projet Pirates des Caraïbes fait appel au concept de la téléopération d'un robot autonome.  Un usager utilise un ordinateur (la station de base) pour acheminer, via un lien sansfil, une commande de haut niveau au robot situé sur un terrain à distance. Avec ses capacités de perception, de locomotion, de préhension et son intelligence, le robot exécute sans intervention humaine la tâche demandée. Le robot envoie un signal à la station de base pour confirmer la fin de l'exécution de la tâche lorsque celle-ci est complétée.

### Dévelopement du projet

Étapes pour initialiser l'environnement de dévelopement :

#### Pour windows :

1.	Installer python 3.4.4 a l'adresse suivante:
		<https://www.python.org/downloads/windows/>
2.	Installer les outils d'environnement virtuel avec la commande suivante :
		```pip install virtualenv```
3.	Installer l'environnement virtuel :
		```virtualenv venv```
4.	Activer l'environnement virtuel :
		```.\venv\Scripts\activate```
5.	Installer sur l'environnement virtuel les dépendances du projet :
		```pip install -r requirements.txt```
6.  Installer numpy 1.10.4 disponible sur <http://www.lfd.uci.edu/~gohlke/pythonlibs/>
7.  Installer OpenCV 3.1.0 disponible au même endroit.
8.	Pour terminer désactiver l'environnement virtuel :
		```deactivate```

Étapes pour le développement :

Dans un terminal:

1.	Executer : ```.\venv\Scripts\activate ```
2.	Executer : ```pip install -r requirements.txt --upgrade``` pour mettre a jour les dépendances
3.	Pour terminer, executer deactivate

Étapes pour exécuter l'application
1.	Executer : ```.\venv\Scripts\activate ``` pour activer l'environnement virtuel
2.	Executer : ```pip install -r requirements.txt --upgrade``` pour mettre a jour les dépendances
3.  Executer les fichier robo_app.py (serveur pour le robot), web_app.py (serveur des fichiers web)
    et base_station_app.py (serveur de la base station). L'interface web est disponible par défaut à localhost:8080

***Pour installer les dépendances pour la webapp voir le fichier webapp/README.md***

Pour mettre à jour la liste de dépendances il faut écrire en UTF-8 les dépendances dans le fichier requirements.txt dans le format suivant :

```
nose==1.3.7
module=version.number
```

###Tests
Afin de rouler les tests d'intégration, il faut démarrer les serveurs du robot et de la station de base. (Exécuter robot_app.py et base_station_app.py)

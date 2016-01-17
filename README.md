Projet de Design III 
## Pirates des Caraïbes
### Description Sommaire
Le projet Pirates des Caraïbes fait appel au concept de la téléopération dun robot autonome.  Un usager utilise un ordinateur (la station de base) pour acheminer, via un lien sansfil, une commande de haut niveau au robot situé sur un terrain à distance. Avec ses capacités de perception, de locomotion, de préhension et son intelligence, le robot exécute sans intervention humaine la tâche demandée. Le robot envoie un signal à la station de base pour confirmer la fin de lexécution de la tâche lorsque celle-ci est complétée.

### Dévelopement du projet

Étapes pour initialiser l'environnement de dévelopement :

#### Pour windows :

1.	Installer python 3.4.4 a l'adresse suivante:
		<https://www.python.org/downloads/windows/>
2.	Installer les outils d'environnement virtuel avec la commande suivante :
		```pip install virtualenv```
3.	Installer l'environnement virtuel :
		```virtualenv venv``
4.	Activer l'environnement virtuel :
		```.\venv\Scripts\activate```
5.	Installer sur l'environnement virtuel les dépendances du projet :
		```pip install -r requirements.txt```
6.	Pour terminer désactiver l'environnement virtuel :
		```deactivate```

Étapes pour le développement :
 
Dans un terminal: 
 
1.	Executer : ```.\venv\Scripts\activate ```
2.	Executer : ```pip install -r requirements.txt --upgrade``` pour mettre a jour les dépendances
3.	Pour terminer, executer deactivate

Pour mettre à jour la liste de dépendances il faut écrire en UTF-8 les dépendances dans le fichier requirements.txt dans le format suivant :

```
nose==1.3.7
module=version.number 
```

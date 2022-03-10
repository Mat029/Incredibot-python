# Incredibot

* IMPORTANT : J'ai migré kivy de la 2.0.0 (qui datait de decembre 2020) à la 2.1.0 (qui date de mars 2022), car elle apporte quelques truc, et nottament plus d'un an de correction de bugs (oui on a de la chance niveau timing).
* On a un problème au niveau des versions. la 2.0.0 suportait 3.6 - 3.9, on utilisait donc la 3.9(.10). Avec la 2.1.0 on passe à 3.7 - 3.10. Il serait alors interessant de passer à la 3.10, qui permait nottament les paternes, intéressant pour notre projet. Cependant thonny lui est bloqué avec une version inclus de 3.7, ce qui nous empêche de passer à 3.10, voir même nous force à migrer... vers une version antérieure. Même si il ne devrait pas y avoir de problème (pas de problèmes majeur en tout cas) lors de la migration du code en arrière, il est toujours problématique de migrer pour "perdre des trucs", alors qu'on pourrait en gagner. 

## Nécessaire:
* Python >=3.7 & <=3.10 
* les trucs de base (pip, setuptools, docutils ...) à jour
* kivy[base] , si qqun a la fois de ts les écrire, sinon pip -m install kivy[base] ça marche

## Doc :

On travaille dessus ça viendra

## En cours/terminé :

* Une interface pour mettre des inputs ✅
* Des boutons pour directement mettre les instruction (voir empêcher l'utilisateur de mettre lui même les instruction, ça éviterai qu'il fasse n'importe quoi) ✅
* Un système qui verifie que les instructions de la personne marche (sinon donner l'erreur) ✅
* Etage 1 ✅
* Un système qui montre les mouvements du robot ⏱ 
* Etage 2 🧠

(Symboles : ✅ : terminer (tester à fond) ❌ : annulé ⏱ : en cours de "coding"/terminé mais buggué 🧠 : en reflexion )

## Road Map  :

### ----------Stric Minimum pour le projet final----------
* Finir les 8 premiers niveaux fonctionnels ✅
* Faire fonctionner le mouvement du robot
* Faire l'étage 2
* Refonte graphique de l'interface des niv (avec des images "clean")
* Faire l'étage 3
* Faire une interface de cours et en rédiger 4
### ----------Objectif----------
* Passer à 8 cours
* Ajouter de la musique/des sons
* Faire l'étage 4
### ----------"Vrai" Objectif----------
* Ajouter des "paramètres"
* Mode "étape par étape"
* Animation des plateaux/du robot
### ----------Bonus cool----------
* Mode multijoueur ou Create (Create est plus "logique" mais multi plus "fun" (et long à coder aussi))
### ----------Si on avait 10ans----------
* Le 2ème mode
* Passage à 6/8 niveaux 
* Vidéo explicative pour chaque cours
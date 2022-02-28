franchement g la flemme de tout lire
tkt c surtout pr Loann ou au cas où tu sais plus à quoi un des trucs sert

# Incredibot
La vraie question c est ce que Loann lira cette ligne un jour.

Faudrait qu'on se fasse une sorte de "doc" interne pour savoir comment le programme marche
Je vais mettre le début :
En gros : ....
Bon on a une classe Incredibot(App) qui returne le fichier .kv, dans lequel il y a un WindowManager. C elle qui est executé quand on lance le programme. Window manager par définition ça gère les différents "écrans" (home, level, le niveau 1 etc ...)
Ttes les classes sont d'abord défini dans le .py, puis la partie graphique est mis dans le .kv et la partie logique à nouveau dans le .py .
On pourrait mettre la logique simple dans le .kv, mais pour l'organisation mieux vaux faire des fonctions dans la classe correspondante qu'on appele par root.mafonction() 
(attention ça passe auto le self, donc quand on déclare une fonction, tjrs mettre self en premier, qu'on est des arguments ou pas).
actuellement (28/02) il y a les systèmes suivant qui ont été implamté par Gazpascho et moi :
La page d'acceuil, 3 bouton , quit ferme la page, cours appele une fonction qui fait "rien" à part print de la merde et levels envoi vers l'écran level.
L'écran level, on a 8 bouton de base + un de retour a home. Le truc d'étafe c une simple variable dans la classe Screen_Levels (ou jsp comment il s'appele).
A chaque fois qu'on appuie sur un btn + ou - pour changer d'étage, ça appele une fonction qui augmente ou réduit de 1 la variable, et mett à jour les textes, 
en vérifiant à chaque fois si il faut bloquer/debloquer un bouton car le max ou le min est atteint/n'est plus atteint
pour les niveau, dès qu'on clique dessus, il nous envoi au niveau du nombre x + 8 * etages. Ainsi tt les identifiants de screen du level sont nommé en fonction du cbème 
ils sont (c pas français mais pg). Avant "d'autoriser" au niveau, il y a une verification qu'on a le droit d'acceder au niveau par le code :
if x + 8 * etages >= lvl max ---> écran du même nom sinon rester sur cet écran
pour obtenir le level max, on fait app.getlvlmax(), une fonction défini dans la classe app, qui récupère la valeur inscit sur le fichier lvlmax.txt
(dans tt ce processus faire gaffe aux string et aux int, les nom d'écrans et la valeur du fichier sont des string
A chaque fois qu'on va dans dans un niveau, cette valeur s'écrit dans un fichier current.txt grace à une fonction
Dans chaque lvl, il y a un bouton back pr revenir aux niveau, un label avc le nom du fichier et un bouton pour valider le niveau (c provisoire tt ça). Il appel alors 
une fonction dans app qui regarde si le niveau actuel (current.txt) est supérieur au niveau max, et si c le cas il le remplace dans le fichier
Il manque sans doute plein de trucs ms pg je completerai plus tard (peut etre)

# DU COUP LA MOITIE EST FAUX G CHANGE PLEIN DE TRUC + JE VAIS PASSER TT EN ECRAN REUTILISABLE POUR LES NIVEAUX
Nécessaire:
_ Python >3.7 <3.10 (je conseille la dernière version de 3.9 (ajd 3.9.10))
_ les trucs de base (pip, setuptools, docutils ...) à jour
_ kivy[base] , si qqun a la fois de ts les écrire, sinon pip -m install kivy[base] ça marche


""""
Pour lancer Incredibot il vous faut :
_ Python >= 3.7.9 
_ Le module kivy : 2 façons de l'installer :
    * Si votre éditeur le supporte (Pycharm, Thonny etc...) installer le "grand" Kivy, avec toutes les dépendances
    * Sinon : pip -m install kivy[base] dans votre terminal
(voir mode d'emploi pour plus d'informations)
"""

from functools import partial
import json
import sys

if sys.version_info < (3,7,9) :
    print("Version de Python incompatible, mettez à jour vers une version compatible (>= 3.7.9)" )
    sys.exit()

""" IMPORTANT : 
Il existe un bug/problème de compatibilité dans kivy qui fait que le programme ne démarre pas sur certains ordinateurs
et affiche une erreur du type : wrong open gl version, you have xx and kivy need xx
Si cela vous arrive, il vous suffit de copier-coller ces deux lignes JUSTE AVANT L'IMPORT DE KIVY :
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
"""
import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

class HomeScreen(Screen):
    """ HomeSreen
    Dans kivy, on déclare chaque écran comme une classe qu'on modifie ensuite avec le fichier .kv
    Cet écran est le premier à apparaître quand on arrive sur incredibot
    Args :
        Screen (Screen) : affiche du contenu
    """
    pass

class LevelScreen(Screen):
    """ LevelScreen
    Cet écran permet la sélection entre les niveaux 
    Args :
        Screen (Screen) : affiche du contenu
    """

    def setLvl(self, lvl):
        """ setLvl
        Cette fonction écrit le niveau sélectionné dans un fichier
        args : 
            int : lvl
        """
        fichier = open("assets/current_lvl.txt", "w")
        fichier.write(str(lvl))
        fichier.close()

    def getLvlMax(self):
        """ getLvlMax
        Cette fonction renvoi le niveau maximum (stocké dans un fichier text) débloqué
        returns :
            int : niveau maximum 
        """
        fichierMax = open("assets/max_level.txt", "r")
        lvlMax = fichierMax.read()
        fichierMax.close()
        return int(lvlMax)

    def getImage(self, lvl):
        """getImage
        Cette fonction permet de savoir quelle image il faut afficher devant un niveau (bloqué, réussi ou jouable), 
        args : 
            int : niveau pour lequel on veut l'image
        return :
            l'image a afficher : valide.png, play.png ou cadenas.png
        """
        lvlMax = self.getLvlMax()
        if lvlMax > lvl:
            return "assets/Images/valide.png"
        elif lvlMax == lvl:
            return "assets/Images/play.png"
        else:
            return "assets/Images/cadenas.png"

    etage = 0  

    """ C'est le numéro de l'étage auquel est actuellement  l'utilisateur. 
    Cette variable est déclaré directement dans la classe car le fichier kv a besoin d'y accéder"""

    def changeEtage(self, sens):
        """ changeEtage
        Cette fonction modifie l'étage où se situe l'utilisateur et met à jour visuellement les composants qui le nécessite
        args :
            str : "augmente", "baisse" ou "aucun" (pour l'initialisation)
        """
        if sens == "augmente":
            self.etage+=1
        elif sens == "baisse": 
            self.etage-=1
        self.ids._boutonAugmente.disabled = (self.etage == 2)
        self.ids._boutonBaisse.disabled = (self.etage == 0)
        self.ids._labelEtage.text = "Etage " + str(self.etage +1)
        self.ids._bouton1.text = "Niveau " + str(self.etage * 8 + 1)
        self.ids._bouton2.text = "Niveau " + str(self.etage * 8 + 2)
        self.ids._bouton3.text = "Niveau " + str(self.etage * 8 + 3)
        self.ids._bouton4.text = "Niveau " + str(self.etage * 8 + 4)
        self.ids._bouton5.text = "Niveau " + str(self.etage * 8 + 5)
        self.ids._bouton6.text = "Niveau " + str(self.etage * 8 + 6)
        self.ids._bouton7.text = "Niveau " + str(self.etage * 8 + 7)
        self.ids._bouton8.text = "Niveau " + str(self.etage * 8 + 8)
        self.ids._Indicateur1.source = self.getImage(self.etage * 8 + 1)
        self.ids._Indicateur2.source = self.getImage(self.etage * 8 + 2)
        self.ids._Indicateur3.source = self.getImage(self.etage * 8 + 3)
        self.ids._Indicateur4.source = self.getImage(self.etage * 8 + 4)
        self.ids._Indicateur5.source = self.getImage(self.etage * 8 + 5)
        self.ids._Indicateur6.source = self.getImage(self.etage * 8 + 6)
        self.ids._Indicateur7.source = self.getImage(self.etage * 8 + 7)
        self.ids._Indicateur8.source = self.getImage(self.etage * 8 + 8)
        self.ids._imageAugmente.source = 'assets/Images/icon/next_icon.png' if (self.etage != 2) else 'assets/Images/icon/next_icon_dark.png'
        self.ids._imageBaisse.source = 'assets/Images/icon/previous_icon.png' if (self.etage != 0) else 'assets/Images/icon/previous_icon_dark.png'

class CustomLevelScreen(Screen):
    """ CustomLevelScrenen
    Cet écran est le plus important de l'application, c'est celui qui affiche l'interface de jeu
    Args :
        Screen (Screen) : affiche du contenu
    """

    def chargement(self):
        """chargement
        Cette fonction va être appelé dès que l'écran est affiché et met à jour visuellement tous les éléments
        (titre, image, limite, mettre les  objet, placer le robot à la bonne position, afficher les boutons en lien 
        avec l'étage (sauter à partir de l'étage 2 par exemple))
        """
        lvl = self.getLvl()
        fichierMax = open("assets/max_level.txt", "r")
        lvlMax = fichierMax.read()
        fichierMax.close()
        DataLvl = self.getLvlJson()
        self.ids._labelNomLvl.text = " Niveau " + str(lvl)
        self.ids._buttonPrevious.disabled = lvl == 1
        self.ids._buttonNext.disabled = int(lvlMax) <= lvl or lvl == 24
        self.ids._imageLvl.source = "assets/Images/lvl/lvl" + str(lvl) + ".png"
        self.ids._labelResultat.text = ""
        self.ids._userInput.text = ""
        self.ids._buttonSauter.disabled = True
        self.ids._buttonSauter.background_color = [0,0,0,0]
        self.ids._buttonSauter.text = ""
        self.ids._buttonAttendre.disabled = True
        self.ids._buttonAttendre.background_color = [0,0,0,0]
        self.ids._buttonAttendre.text = ""
        self.ids._buttonPrendre.disabled = True
        self.ids._buttonPrendre.background_color = [0,0,0,0]
        self.ids._buttonPrendre.text = ""
        if lvl >= 9:
            self.ids._buttonSauter.disabled = False
            self.ids._buttonSauter.background_color = [1,1,1,1]
            self.ids._buttonSauter.text = "Sauter"
            self.ids._buttonAttendre.disabled = False
            self.ids._buttonAttendre.background_color = [1,1,1,1]
            self.ids._buttonAttendre.text = "Attendre"
        if lvl >= 17:
            self.ids._buttonPrendre.disabled = False
            self.ids._buttonPrendre.background_color = [1,1,1,1]
            self.ids._buttonPrendre.text = "Prendre/Deposer"
        posRobot = self.posToCoord(DataLvl["d"])
        self.robot = Image(source = "assets/Images/robot/robot_droite_sans.png", size_hint =  [.066796875 , .11875],pos_hint = posRobot)
        self.ids._layoutLvl.add_widget(self.robot)
        if "limite" in DataLvl:
            self.ids._labelInstruction.text = "Instructions : 0 / " + str(DataLvl["limite"]) 
        else:
            self.ids._labelInstruction.text = "Instructions : 0 / ∞"
        if "nbObjets" in DataLvl:
            posObjet0 = self.posToCoord( DataLvl["dObjet0"])
            self.obj0 = Image(source = "assets/Images/lvl/objet0.png", size_hint =  [.066796875 , .11875],pos_hint = posObjet0, allow_stretch = True)
            self.ids._layoutLvl.add_widget(self.obj0)
            if DataLvl["nbObjets"] >= 2:
                posObjet1 = self.posToCoord( DataLvl["dObjet1"])
                self.obj1 = Image(source = "assets/Images/lvl/objet1.png", size_hint =  [.066796875 , .11875],pos_hint = posObjet1, allow_stretch = True)
                self.ids._layoutLvl.add_widget(self.obj1)
            if DataLvl["nbObjets"] == 3:
                posObjet2 = self.posToCoord( DataLvl["dObjet2"])
                self.obj2 = Image(source = "assets/Images/lvl/objet2.png", size_hint =  [.066796875 , .11875],pos_hint = posObjet2, allow_stretch = True)
                self.ids._layoutLvl.add_widget(self.obj2)

        self.sound = SoundLoader.load("assets/Sound/empty.mp3")  # Initialise le son pour pouvoir jouer des sons plus tard

    def getLvl(self):
        """ getLvl
        Cette fonction retourne le niveau actuel
        returns :
        int : lvl : niveau actuel
        """
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        fichierLvl.close
        return int(lvl)

    def getLvlJson(self):
        """ getLvlJson
        Cette fonction renvoi les donnés associées au niveau stocké dans le json
        returns :
            dictionary : DataLvl : les données Json du niveau actuel
        """
        lvl = self.getLvl()
        MyJson = open('assets/data.json',encoding="utf-8")
        Data = json.load(MyJson)
        MyJson.close()
        DataLvl = Data[lvl - 1]
        return DataLvl

    def setLvl(self, lvl):
        """ setLvl
        Cette fonction change le niveau actuel
        args :
            lvl : int : le niveau qui va devenir le niveau actuel"""
        fichier = open("assets/current_lvl.txt", "w")
        fichier.write(str(lvl))
        fichier.close()

    def clean(self):
        """ clean
        Cette fonction supprime tous les éléments rajouté (robot et objets)
        """
        DataLvl = self.getLvlJson()
        Animation.cancel_all(self.robot)
        self.ids._layoutLvl.remove_widget(self.robot)
        if "nbObjets" in DataLvl:
            Animation.cancel_all(self.obj0)
            self.ids._layoutLvl.remove_widget(self.obj0)
            if DataLvl["nbObjets"] >= 2:
                Animation.cancel_all(self.obj1)
                self.ids._layoutLvl.remove_widget(self.obj1)
            if DataLvl["nbObjets"] == 3:
                Animation.cancel_all(self.obj2)
                self.ids._layoutLvl.remove_widget(self.obj2)

    def delLine(self, texte):
        """ delLine
        Cette fonction est appelée quand on appuie sur le bouton supprimer, 
        elle enlève la dernière ligne du texte 
        args :
            str : texte : les instructions rentrés par l'utilisateur
        returns :
            str : texteFinal : les instructions de l'utilisateurs avec une ligne en moins
        """
        if texte!= "":
            texteCoupe = texte.splitlines()
            del texteCoupe[-1]
            texteFinal = "\n".join(texteCoupe)
            return (texteFinal)
        else:
            return ""

    def prendreDeposer(self, texte):
        """ prendreDeposer
        Quand on appuie sur le bouton Prendre/Déposer, cette fonction calcule lequel elle doit écrire
        args :
            str : texte: les instructions rentrés par l'utilisateur
        returns :
            str : l'instruction a ajouté : Prendre ou Déposer
        """
        texte = texte.lower()
        texteCoupe = texte.splitlines()
        nbPrendreDepose = 0
        for instruction in texteCoupe:
            if instruction == "prendre" or instruction == "déposer":
                nbPrendreDepose +=1
        if nbPrendreDepose%2 == 1:
            return "\nDéposer"
        else:
            return "\nPrendre"
    def indice(self):
        """ indice
        Cette fonction est appelée quand le bouton indice est cliqué, et affiche à l'écran l'indice du niveau s'il existe
        """
        DataLvl = self.getLvlJson()
        if "indice" in DataLvl:
            self.ids._labelResultat.text = DataLvl["indice"]
        else:
            self.ids._labelResultat.text = "Pas d'indice pour ce niveau"
        
    def cancel(self):
        """"cancel
        Cette fonction est appelée quand on clique sur le bouton annuler. Elle remet les éléments du niveau a leur position initiale.
        """
        DataLvl = self.getLvlJson()
        Animation.cancel_all(self.robot)
        self.robot.pos_hint = self.posToCoord(DataLvl["d"])
        self.robot.source = "assets/Images/robot/robot_droite_sans.png"
        if "nbObjets" in DataLvl:
            Animation.cancel_all(self.obj0)
            self.obj0.pos_hint = self.posToCoord( DataLvl["dObjet0"])
            if DataLvl["nbObjets"] >= 2:
                Animation.cancel_all(self.obj1)
                self.obj1.pos_hint = self.posToCoord( DataLvl["dObjet1"])
                if DataLvl["nbObjets"] == 3:
                    Animation.cancel_all(self.obj2)
                    self.obj2.pos_hint = self.posToCoord( DataLvl["dObjet2"])
        self.sound.stop()

    def nbInstructions(self, texte):
        """ nbInsructions
        Cette fonction est appelée à chaque fois que l'on écrit, elle calcule le nombre d'instructions
        et vérifie qu'elle ne dépasse pas la limite du niveau (50 par défaut)
        args : 
            str : texte: les instructions rentrés par l'utilisateur
        """
        DataLvl = self.getLvlJson()
        texteCoupe = texte.splitlines()
        limiteStr = "∞"
        limite = 50
        if "limite" in DataLvl:
            limite = DataLvl["limite"]
            limiteStr =  str(limite)
        if len(texteCoupe) > limite:
            self.ids._labelInstruction.color = [1,0,0,1]
        else:
            self.ids._labelInstruction.color = [1,1,1,1]
        self.ids._labelInstruction.text = " Instructions : " + str(len(texteCoupe)) + " / " + limiteStr

    def play(self, texte):
        """ play 
        Cette fonction est la première appelée quand on clique sur le bouton play
        Elle s'occupe des animations jusqu'à ce que le robot soit sur sa position final
        Ce n'est pas elle qui calcule le parcours, c'est une autre fonction : verif
        Elle se contente de faire bouger les objets en fonction des résultats, 
        en appelant finAnim pour faire revenir les objets à leur place , afficher le message et jouer le son
        args :
            str : texte: les instructions rentrés par l'utilisateur
        """
        listePos, listePosObjets, listeOrientation, listeObjet, message, son = self.verif(texte)
        nbObjet = len(listePosObjets)
        Animation.cancel_all(self.robot)
        self.robot.source = "assets/Images/robot/robot_droite_sans.png"
        self.sound.stop()

        def animerRobot(orientation, objet, robot):
            """ animerRobot
            Cette fonction change l'image du robot pour montrer l'orientation/ les objets du robot
            Cette fonction dans une fonction était nécessaire pour faire changer l'image du robot car le module animation
            que l'on utilise pour faire bouger le robot ne peut pas faire changer l'image. 
            args :
                orientation : int : le sens du robot
                objet : str ou int : si le robot tient un objet/lequel
                robot : l'objet kivy sur lequel on applique le changement d'image
            """
            traductionOrientation = {1: "droite", -1: "gauche", 10: "bas", -10: "haut"}
            traductionObjet = {"sans": "sans", 0: "bleu", 1: "violet", 2: "rouge"}
            robot.source = "assets/Images/robot/robot_" + traductionOrientation[orientation] + "_" + traductionObjet[objet] + ".png"

        anim = Animation(pos_hint =self.posToCoord(listePos[0]), duration = 0)
        if nbObjet > 0:
            Animation.cancel_all(self.obj0)
            animObj0 = Animation(pos_hint =self.posToCoord(listePosObjets[0][0]), duration = 0)
            if nbObjet >= 2:
                Animation.cancel_all(self.obj1)
                animObj1 = Animation(pos_hint =self.posToCoord(listePosObjets[1][0]), duration = 0)
                if nbObjet == 3:
                    Animation.cancel_all(self.obj2)
                    animObj2 = Animation(pos_hint =self.posToCoord(listePosObjets[2][0]), duration = 0)
        if len(listePos) >= 1:
            for i in range(1, len(listePos)):
                coordoneei = self.posToCoord(listePos[i])
                coordoneeimoins = self.posToCoord(listePos[i - 1])
                coordoneeFinal = {"center_x": (coordoneei["center_x"] + coordoneeimoins["center_x"])/2, "center_y": (coordoneei["center_y"] + coordoneeimoins["center_y"])/2} #permet de faire une moitié de l'animation
                animProvisoire = Animation(pos_hint = coordoneeFinal, duration = .25)
                animProvisoire.on_complete = partial(animerRobot, listeOrientation[i], listeObjet[i])
                anim += animProvisoire
                animProvisoire2 = Animation(pos_hint = coordoneei, duration = .25)
                anim += animProvisoire2
                if nbObjet > 0:
                    if listePosObjets[0][i - 1] == listePosObjets[0][i]:
                        animObj0 += Animation(duration = .5)
                    else: 
                        animObj0 += Animation(pos_hint =self.posToCoord(listePosObjets[0][i - 1]), duration = .25)
                        animObj0 += Animation(pos_hint =self.posToCoord(listePosObjets[0][i]), duration = 0) #permet a l'objet d'apparaitre/disparaitre instant
                        animObj0 += Animation(pos_hint =self.posToCoord(listePosObjets[0][i]), duration = .25) 
                    if nbObjet >= 2:
                        if listePosObjets[1][i - 1] == listePosObjets[1][i]:
                            animObj1 += Animation(duration = .5)
                        else: 
                            animObj1 += Animation(pos_hint =self.posToCoord(listePosObjets[1][i - 1]), duration = .25)
                            animObj1 += Animation(pos_hint =self.posToCoord(listePosObjets[1][i]), duration = 0)
                            animObj1 += Animation(pos_hint =self.posToCoord(listePosObjets[1][i]), duration = .25) 
                        if nbObjet == 3:
                            if listePosObjets[2][i - 1] == listePosObjets[2][i]:
                                animObj2 += Animation(duration = .5)
                            else: 
                                animObj2 += Animation(pos_hint =self.posToCoord(listePosObjets[2][i - 1]), duration = .25)
                                animObj2 += Animation(pos_hint =self.posToCoord(listePosObjets[2][i]), duration = 0)
                                animObj2 += Animation(pos_hint =self.posToCoord(listePosObjets[2][i]), duration = .25) 
            anim.on_complete = partial(self.finAnim , message, listePos, listePosObjets, son)
        anim.start(self.robot)
        if nbObjet >0:
            animObj0.start(self.obj0)
            if nbObjet >= 2:
                animObj1.start(self.obj1)
                if nbObjet == 3:
                    animObj2.start(self.obj2)

    def finAnim(self, message, listePos, listePosObjets, son, *args):
        """ finAnim
        Cette fonction est appelée quand l'animation est finie, pour faire revenir les éléments à leur place, afficher le message et jouer le son
        Elle vérifie aussi si les Icones pour changer d'étage rapidement doivent être activé (si on a réussi le niveau)
        args : 
            message : str : le message de réussite/ d'échec a affiché
            listePos : liste : la liste des positions du robot pendant son parcours
            listePosObjets : liste : la liste des position des objets pendant le parcours du robot
            son : str : le chemin d'accès vers le son a joué
        """
        lvl = self.getLvl()
        nbObjets = len(listePosObjets)
        fichierMax = open("assets/max_level.txt", "r")
        lvlMax = fichierMax.read()
        fichierMax.close()
        self.ids._labelResultat.text = message
        self.ids._buttonNext.disabled = int(lvlMax) <= lvl or lvl == 24
        if len(listePos) >= 1:
            def resetImage(*args):
                self.robot.source = "assets/Images/robot/robot_droite_sans.png"
            anim3= Animation(pos_hint = self.posToCoord(listePos[len(listePos) - 1]), duration =  2.5)
            anim3 += Animation(pos_hint =self.posToCoord(listePos[0]), duration = 0)
            anim3.on_complete = resetImage
            anim3.start(self.robot)
        if nbObjets >= 1:
            anim4= Animation(pos_hint = self.posToCoord(listePosObjets[0][len(listePosObjets[0]) - 1]), duration =  2.5)
            anim4 += Animation(pos_hint =self.posToCoord(listePosObjets[0][0]), duration = 0)
            anim4.start(self.obj0)
            if nbObjets >= 2:
                anim5= Animation(pos_hint = self.posToCoord(listePosObjets[1][len(listePosObjets[1]) - 1]), duration =  2.5)
                anim5 += Animation(pos_hint =self.posToCoord(listePosObjets[1][0]), duration = 0)
                anim5.start(self.obj1)
                if nbObjets == 3:
                    anim6= Animation(pos_hint = self.posToCoord(listePosObjets[2][len(listePosObjets[2]) - 1]), duration =  2.5)
                    anim6 += Animation(pos_hint =self.posToCoord(listePosObjets[2][0]), duration = 0)
                    anim6.start(self.obj2)
        JsonSettings = open('assets/settings.json',)
        SettingsData = json.load(JsonSettings)
        JsonSettings.close()
        if son != "" and SettingsData["son"]:
            self.sound = SoundLoader.load(son)
            self.sound.volume = SettingsData["sonVolume"]
            self.sound.play()

    def posToCoord(self, pos):
        """ posToCoord
        Cette fonction est centrale dans le programme. Pour calculer la position du robot, on utilise un système de grille avec des 
        cases qui vont de 11 à 88 (le premier chiffre est la ligne, qu'on compte de haut en bas et le deuxième la colonne,
        qu'on compte de gauche à droite. Cette fonction 'traduit' ce numéro de grille en coordonnée

        Voila le calcul qu'effectue la fonction de façon plus ou moins compréhensible par un humain :
        center_x : début de l'image + demi case  + unité de la pos * taille d'un carreau 
        center_y : début de l'image + demi carreau +  dizaine de la pos * taille d'un carreau

        args: 
            pos : int : la position, selon la notation de la grille
        returns:
            dictionary : la position de l'objet près pour l'affichage de kivy
        """

        return {"center_x": (0.455625 + 0.0333984375 + ((pos%10 - 1) * 0.066796875)), "center_y": (0.025 + 0.059375 + ((8 - (pos//10)) * 0.11875))} 

    def verif(self,texte):
        """verif
        Cette fonction est le véritable algorithme qui vérifie les instructions de l'utilisateur
        Il exécute et vérifie toutes les instructions, en ajoutant la positon/l'orientation/les objets dans des liste
        Il renvoi ensuite toutes les données nécessaires pour l'affichage du résultat
        args : 
            str : texte: les instructions rentrés par l'utilisateur
        returns :
            listePosRobot : liste : la liste des positions du robot pendant son parcours
            listePosObjets : liste : la liste des positions des objets pendant le parcours du robot
            listeOrientation : liste : la liste des orientation du robot pendant son parcours
            listeObjet : liste : liste des objet tenu par le robot pendant son parcours
            message : str : le message de réussite/ d'échec a affiché
            son : str : le chemin d'accès vers le son a joué
        """
        lvl = self.getLvl()
        DataLvl = self.getLvlJson()
        texte = texte.lower()
        listeInstructions = texte.splitlines()
        listePosRobot = []
        listeOrientation = []
        listeObjet = []
        listePosObjets = []
        posObjets = []
        message = "ECHEC : Il manque une/des instruction(s)"
        son = "assets/Sound/fail.mp3"
        posRobot = DataLvl["d"]
        listePosRobot.append(posRobot)
        orientationRobot = 1
        listeOrientation.append(orientationRobot)
        objet = {"tenir": False, "numero": 0}
        listeObjet.append("sans")
        cyleOrientation = {1: 10, 10: -1, -1: -10, -10: 1} # Permet de changer l'orientation sans avoir à faire 40 milles if/elif, initialement orienté pour tourner à droite
        cycleTapis = {"t-d": 1, "t-g": -1, "t-h": -10, "t-b": 10}
        if "nbObjets" in DataLvl: 
            posObjets = [DataLvl["dObjet" + str(s)] for s in range(DataLvl["nbObjets"])]
            listePosObjets = [[s] for s in posObjets]
        terminer = ("limite" in DataLvl and DataLvl["limite"] < len(listeInstructions) or (len(listeInstructions) > 50))
        if terminer:
            message = "ECHEC : Limite d'instructions dépassé"
            son = "assets/Sound/error.mp3"
        nbExecution = 0
        while not terminer and nbExecution < len(listeInstructions):
            instruction = listeInstructions[nbExecution]
            if instruction == "avancer":
                posRobot += orientationRobot
            elif instruction == "reculer":
                posRobot -= orientationRobot
            elif instruction == "droite":
                orientationRobot = cyleOrientation[orientationRobot]
            elif instruction == "gauche":
                orientationRobot = - cyleOrientation[orientationRobot]
            elif instruction == "attendre" and lvl >= 9:
                pass
            elif instruction == "sauter" and lvl >= 9:
                if str(posRobot + orientationRobot) in DataLvl:
                    terminer = True
                    message = "ECHEC : Tu ne peut sauter que par dessus le vide"
                    son = "assets/Sound/impossible.mp3"
                else:
                    posRobot += 2 * orientationRobot
            elif instruction == "prendre" and lvl >= 17:
                if "nbObjets" in DataLvl and (posRobot + orientationRobot) in posObjets:
                    if objet["tenir"]:
                        terminer = True
                        message = "ECHEC : Tu tiens déjà un objet"
                        son = "assets/Sound/impossible.mp3"
                    else: 
                        objet["tenir"] = True
                        objet["numero"] = posObjets.index((posRobot + orientationRobot))
                        posObjets[objet["numero"]] = 0
                else:
                    terminer = True
                    message = "ECHEC : Il n'y a pas d'objet à prendre"
                    son = "assets/Sound/impossible.mp3"
            elif instruction == "déposer" and lvl >= 17:
                if "nbObjets" in DataLvl and objet["tenir"]:
                    if str(posRobot + orientationRobot) in DataLvl and DataLvl[str(posRobot + orientationRobot)] in ["c","f"] and (posRobot + orientationRobot) not in posObjets:
                        objet["tenir"] = False
                        posObjets[objet["numero"]] = posRobot + orientationRobot
                    else:
                        terminer = True
                        message = "ECHEC : Tu ne peux pas poser d'objet ici"
                        son = "assets/Sound/impossible.mp3"
                else:
                    terminer = True
                    message = "ECHEC : Tu n'as pas d'objet à poser"
                    son = "assets/Sound/impossible.mp3"
            elif instruction == "#tricher":
                    terminer = True
                    son = "assets/Sound/boo.mp3"
                    message = "Tricher c'est mal !!!"
                    fichierMax = open("assets/max_level.txt", "r+")
                    fichierMax.seek(0)
                    fichierMax.truncate()
                    fichierMax.write("24")
                    fichierMax.close()
            else:
                terminer = True
                message = "ECHEC : Mot incorrect dans le script"
                son = "assets/Sound/impossible.mp3"
            listePosRobot.append(posRobot)
            listeOrientation.append(orientationRobot)
            for c in range(len(listePosObjets)):
                listePosObjets[c].append(posObjets[c])
            if objet["tenir"]:
                listeObjet.append(objet["numero"])
            else: 
                listeObjet.append("sans")
            if str(posRobot) in DataLvl:
                if "tp" in DataLvl[str(posRobot)]:
                    posRobot = int(DataLvl[str(posRobot)][-2:])
                    listePosRobot.append(posRobot)
                    listeOrientation.append(orientationRobot)
                    for c in range(len(listePosObjets)):
                        listePosObjets[c].append(posObjets[c])
                    if objet["tenir"]:
                        listeObjet.append(objet["numero"])
                    else: 
                        listeObjet.append("sans")         
                elif "t-" in DataLvl[str(posRobot)]:
                    posRobot += cycleTapis[DataLvl[str(posRobot)]]
                    listePosRobot.append(posRobot)
                    listeOrientation.append(orientationRobot)
                    for c in range(len(listePosObjets)):
                        listePosObjets[c].append(posObjets[c])  #(nécessaire pour que les anims des objets et le robot soit synchro)
                    if objet["tenir"]:
                        listeObjet.append(objet["numero"])
                    else: 
                        listeObjet.append("sans")
                if str(posRobot) in DataLvl:
                    if not (posRobot in posObjets):
                        if DataLvl[str(posRobot)] == "f" and (nbExecution +1) == len(listeInstructions):
                            terminer = True
                            succes = True
                            nbObjets = len(posObjets)
                            while succes and nbObjets > 0:
                                succes = (posObjets[nbObjets - 1] == DataLvl["fObjet" + str(nbObjets - 1)]) 
                                nbObjets -=1
                            if succes:
                                message = "REUSSI : Bravo, tu as réussi le niveau " + str(lvl)
                                son = "assets/Sound/victory.mp3"
                                if lvl == 24:
                                    message = "REUSSI : Félicitation, tu as réussi tous les niveaux !!!"
                                    son = "assets/Sound/fini.mp3"
                                fichierMax = open("assets/max_level.txt", "r+")
                                if (lvl +1) > int(fichierMax.read()):
                                    fichierMax.seek(0)
                                    fichierMax.truncate()
                                    fichierMax.write(str(lvl +1))
                                fichierMax.close()
                            else:
                                message = "ECHEC : Un objet n'est pas à sa place "
                                son = "assets/Sound/fail.mp3"
                    else:
                        terminer = True
                        message = "ECHEC : Tu ne peux pas traverser un objet"
                        son = "assets/Sound/punch.mp3"
                else: 
                    terminer = True
                    message = "ECHEC : Tu sors du parcours"
                    son = "assets/Sound/fall.mp3"
            else:
                terminer = True
                message = "ECHEC : Tu sors du parcours"
                son = "assets/Sound/fall.mp3"
            nbExecution += 1
        return listePosRobot, listePosObjets, listeOrientation, listeObjet, message, son
        
class CoursScreen(Screen):
    """ CoursScreen
    Cet écran permet la sélection entre les cours 
    Args :
        Screen (Screen) : affiche du contenu
    """
    def setCours(self, cours):
        """ setCours
        Cette fonction change le cours qu'on va voir
        args :
            cours : int : le numéro du cours que l'on va voir
        """
        fichier = open("assets/current_cours.txt", "w")
        fichier.write(cours)
        fichier.close()

class CustomCoursScreen(Screen):
    """ CustomCoursScreen
    Cet écran est l'écran de base des cours qui est réutilisé à chaque fois que l'on va sur un cours
    Args :
        Screen (Screen) : affiche du contenu
    """
    def chargementCours(self):
        """chargement
        Cette fonction va être appelée dès que l'écran est affiché et met à jour visuellement le texte/les images a affichés
        """
        fichier_cours = open("assets/current_cours.txt", "r")
        cours = fichier_cours.read()
        fichier_cours.close()
        fichier_text = open("assets/Cours/cours_" + cours + ".txt", "r", encoding="utf8")
        texte = fichier_text.read()
        fichier_text.close()
        self.ids._labelCours.text = texte
        self.ids._imageCours.source = "assets/Images/cours/img_cours_" + str(cours) + ".png"
        self.ids._imageCours2.source = "assets/Images/cours/img_cours_" + str(cours) + "1.png"

class WindowManager(ScreenManager):
    """ WindowManager
    Ce composant est appelé au démarrage de l'application, c'est lui qui gère quel écran affiché
    Args :
        SreenManager (SreenManager) : gère l'affichage des écrans
    """
    pass

class Incredibot(App):
    """ Incredibot
    C'est la base de l'application, qui initialise tous ces composants et affiche la fenêtre de l'application
    Args :
        App(App) : classe qui s'exécute quand on lance l'app
    """

    def build(self):
        """build
        La première fonction à être appelé quand l'application se lance, elle définit les propriétés de la fenêtre (et lance la musique)
        """
        self.title = 'Incredibot'
        self.icon = 'assets/Images/icon.png'
        self.music = SoundLoader.load("assets/Sound/music.mp3")
        JsonSettings = open('assets/settings.json',)
        SettingsData = json.load(JsonSettings)
        JsonSettings.close()
        self.music.loop = True
        self.music.volume = SettingsData["musiqueVolume"]
        if SettingsData["musique"]:
            self.music.play()
        kv = Builder.load_file("main.kv")
        return kv

    def getVolumeMusic(self):
        """ getVolumeMusic
        Cette fonction renvoi le volume de la musique défini dans data.json
        returns :
            float : volume de la musique
        """
        JsonSettings = open('assets/settings.json',)
        SettingsData = json.load(JsonSettings)
        JsonSettings.close()
        return SettingsData["musiqueVolume"]

    def getVolumeSon(self):
        """ getVolumeSon
        Cette fonction renvoi le volume des effets sonores défini dans data.json
        returns :
            float : volume des effets sonores
        """
        JsonSettings = open('assets/settings.json',)
        SettingsData = json.load(JsonSettings)
        JsonSettings.close()
        return SettingsData["sonVolume"]

    def getMusicState(self):
        """ getMusicState
        Cette fonction renvoi les valeurs que doivent prendre les boutons qui permette de couper la musique
        returns:
            tuple : l'état des boutons qui permette de couper la musique
        """
        JsonSettings = open('assets/settings.json',)
        SettingsData = json.load(JsonSettings)
        JsonSettings.close()
        if SettingsData["musique"]:
            return("down","normal")
        else: 
            return ("normal", "down")

    def getSonState(self):
        """ getSonState
        Cette fonction renvoi les valeurs que doivent prendre les boutons qui permette de couper les effets sonores
        returns:
            tuple : l'état des boutons qui permette de couper les effets sonores
        """
        JsonSettings = open('assets/settings.json',)
        SettingsData = json.load(JsonSettings)
        JsonSettings.close()
        if SettingsData["son"]:
            return("down","normal")
        else: 
            return ("normal", "down")

    def changeVolumeSon(self,*args):
        """ changeVolumeSon
        Cette fonction change le volume des effets sonores à partir du slider des paramètres
        args:
            liste : toutes les infos du slider ([0] : l'identifiant de l'objet, [1] : sa valeur)
        """
        JsonSettings = open('assets/settings.json',"r+")
        SettingsData = json.load(JsonSettings)
        SettingsData["sonVolume"] = args[1]
        JsonSettings.seek(0)
        JsonSettings.write(json.dumps(SettingsData))
        JsonSettings.truncate()
        JsonSettings.close()

    def changeVolumeMusic(self,*args):
        """ changeMusSon
        Cette fonction change le volume de la musique à partir du slider des paramètres
        args:
            liste : toutes les infos du slider ([0] : l'identifiant de l'objet, [1] : sa valeur)
        """
        JsonSettings = open('assets/settings.json',"r+")
        SettingsData = json.load(JsonSettings)
        SettingsData["musiqueVolume"] = args[1]
        JsonSettings.seek(0)
        JsonSettings.write(json.dumps(SettingsData))
        JsonSettings.truncate()
        JsonSettings.close()
        self.music.volume = args[1]

    def changeMusic(self, state, element):
        """ changeMusic
        Cette fonction permet de couper/ d'activer la musique
        args:
            state : str : état du bouton (down ou normal)
            element : str : type du bouton (Oui ou non)
        """
        JsonSettings = open('assets/settings.json',"r+")
        SettingsData = json.load(JsonSettings)
        if (state == "down" and element == "Oui") or (state == "normal" and element == "Non"):
            SettingsData["musique"] = True
            self.music.play()
        else: 
            SettingsData["musique"] = False
            self.music.stop()
        JsonSettings.seek(0)
        JsonSettings.write(json.dumps(SettingsData))
        JsonSettings.truncate()
        JsonSettings.close()

    def changeSon(self, state, element):
        """ changeSon
        Cette fonction permet de couper/ d'activer les effets sonores
        args:
            state : str : état du bouton (down ou normal)
            element : str : type du bouton (Oui ou non)
        """
        JsonSettings = open('assets/settings.json',"r+")
        SettingsData = json.load(JsonSettings)
        if (state == "down" and element == "Oui") or (state == "normal" and element == "Non"):
            SettingsData["son"] = True
        else:
            SettingsData["son"] = False
        JsonSettings.seek(0)
        JsonSettings.write(json.dumps(SettingsData))
        JsonSettings.truncate()
        JsonSettings.close()

    def resetSettings(self):
        """ resetSettings
        Cette fonction remet les paramètres de l'application aux paramètres par défauts
        """
        JsonSettings = open('assets/settings.json', "r+")
        SettingsData = {'musique': True, 'musiqueVolume': 0.5, 'son': True, 'sonVolume': 0.8}
        JsonSettings = open('assets/settings.json', "r+")
        JsonSettings.seek(0)
        JsonSettings.write(json.dumps(SettingsData))
        JsonSettings.truncate()
        JsonSettings.close()
        self.music.volume = 0.5
        self.music.play()

    def close_application(self):
        """ close_application
        Cette fonction est appelée quand on appuie sur le bouton quiter et permet de quitter l'application
        """
        App.get_running_app().stop()
        Window.close()

    def on_stop(self):
        """ on_stop
        Cette fonction (qui est en fait un évènement) est appelée dès qu'on appuie sur la croix de la fenêtre pour quitter l'application. 
        Le rajout de Window.close() à cet évènement permet à l'application de se fermer correctement sur tout les ide.
        """
        Window.close()


if __name__ == "__main__":
    """ Règles certains paramètres quand on lance l'application"""
    kivy.require("2.1.0")  # vérifie la version de kivy
    Config.set("input", "mouse", "mouse,multitouch_on_demand")  # permet de désactiver le mode multi touches
    Window.maximize()  # permet de lancer la fenêtre en taille maximal
    Incredibot().run() #lance l'application quand on clique sur run (ou lancer)

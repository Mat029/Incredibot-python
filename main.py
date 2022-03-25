""""
DOC PROVISOIRE !!!!
Voir ttes les recommandations précises dans readme sinon :
installer Kivy :
1) pip -m install kivy[base] dans votre terminal
2) Si votre éditeur le supporte (Pycharme/Thonny, Anaconda aussi je crois etc...) Vous pouvez installer directement kivy. Bien prendre le "grand" Kivy, avec toutes les dépendances.
ATTENTION IMPORTANT :
1) Version de python utilisé : 3.7.9 (compatible avec les versions supérieurs aussi)
2) Un bug de kivy qui affecte nottament les pc de l'écoles, detecte une version d'open Gl qui n'est pas la bonne, ce qui provoque un crash. Dans ce cas, rajouter :
 import os
 os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
 AU TOUT DEBUT DU FICHIER (avant les autres import)
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.animation import Animation
from functools import partial
from kivy.core.window import Window
from kivy.config import Config
import kivy
import json

kivy.require("2.1.0")

class HomeScreen(Screen):
    pass

class LevelScreen(Screen):
    etage = 0
    def update(self):
        self.ids._Indicateur1.source = self.getImage((self.etage * 8 + 1))
        self.ids._Indicateur2.source = self.getImage((self.etage * 8 + 2))
        self.ids._Indicateur3.source = self.getImage((self.etage * 8 + 3))
        self.ids._Indicateur4.source = self.getImage((self.etage * 8 + 4))
        self.ids._Indicateur5.source = self.getImage((self.etage * 8 + 5))
        self.ids._Indicateur6.source = self.getImage((self.etage * 8 + 6))
        self.ids._Indicateur7.source = self.getImage((self.etage * 8 + 7))
        self.ids._Indicateur8.source = self.getImage((self.etage * 8 + 8))
    def setLvl(self, lvl):
        fichier = open("assets/current_lvl.txt", "w")
        fichier.write(str(lvl))
        pass
    def getLvlMax(self):
        fichierMax = open("assets/max_level.txt", "r")
        lvlMax = fichierMax.read()
        return lvlMax
    def getImage(self, lvl):
        lvlMax = int(self.getLvlMax())
        if lvlMax > lvl :
            return "Images/valide.png"
        elif lvlMax == lvl :
            return "Images/play.png"
        else:
            return "Images/cadenas.png"

    def augmente(self):
        self.etage+=1
        self.ids._boutonAugmente.disabled = (self.etage == 3)
        self.ids._boutonBaisse.disabled = (self.etage == 0)
        self.ids._labelEtage.text = str(self.etage +1)
        self.ids._bouton1.text = "Niveau " + str(self.etage * 8 + 1)
        self.ids._bouton2.text = "Niveau " + str(self.etage * 8 + 2)
        self.ids._bouton3.text = "Niveau " + str(self.etage * 8 + 3)
        self.ids._bouton4.text = "Niveau " + str(self.etage * 8 + 4)
        self.ids._bouton5.text = "Niveau " + str(self.etage * 8 + 5)
        self.ids._bouton6.text = "Niveau " + str(self.etage * 8 + 6)
        self.ids._bouton7.text = "Niveau " + str(self.etage * 8 + 7)
        self.ids._bouton8.text = "Niveau " + str(self.etage * 8 + 8)
        self.update()
    def baisse(self):
        self.etage-=1
        self.ids._boutonAugmente.disabled = (self.etage == 3)
        self.ids._boutonBaisse.disabled = (self.etage == 0)
        self.ids._labelEtage.text = str(self.etage +1)
        self.ids._bouton1.text = "Niveau " + str(self.etage * 8 + 1)
        self.ids._bouton2.text = "Niveau " + str(self.etage * 8 + 2)
        self.ids._bouton3.text = "Niveau " + str(self.etage * 8 + 3)
        self.ids._bouton4.text = "Niveau " + str(self.etage * 8 + 4)
        self.ids._bouton5.text = "Niveau " + str(self.etage * 8 + 5)
        self.ids._bouton6.text = "Niveau " + str(self.etage * 8 + 6)
        self.ids._bouton7.text = "Niveau " + str(self.etage * 8 + 7)
        self.ids._bouton8.text = "Niveau " + str(self.etage * 8 + 8)
        self.update()
    pass

class CustomLevelScreen(Screen):
    def chargement(self):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        self.ids._labelNomLvl.text = "Niveau " + lvl
        self.ids._imageLvl.source = "Images/lvl/lvl" + lvl + ".png"
        self.ids._labelResultat.text = ""
        self.ids._userInput.text = ""
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        if int(lvl) <= len(Data) :
                posRobot = self.posToCoord(self.getOrigin(lvl))
                self.robot = Image(source = "Images/lvl/robot.png", size_hint =  [.050625 , .09],pos_hint = posRobot)
                self.ids._layoutLvl.add_widget(self.robot)
                if "limite" in Data[int(lvl) - 1] :
                    self.ids._labelInstruction.text = "Nombre max d'instructions : " + str(Data[int(lvl) - 1]["limite"])
                else:
                    self.ids._labelInstruction.text = "Nombre max d'instructions : NAN"
    def clean(self):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        if int(lvl) <= len(Data) :
            self.ids._layoutLvl.remove_widget(self.robot)
    def changeLvlMax(self):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        fichierMax = open("assets/max_level.txt", "r+")
        if (int(lvl) +1) > int(fichierMax.read()):
            fichierMax.seek(0)
            fichierMax.truncate()
            fichierMax.write(str(int(lvl) +1))
    def getOrigin(self, lvl) :
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        for i in Data[int(lvl) - 1] :
            if Data[int(lvl) - 1][i] == "d" :
                return int(i)
    def play(self, texte) :
        listePos, message = self.verif(texte)
        if len(listePos) >= 1 :
            Animation.stop_all(self.robot)
            anim = Animation(pos_hint =self.posToCoord(listePos[0]), duration = 0)
            for i in range(1, len(listePos)) :
                anim += Animation(pos_hint =self.posToCoord(listePos[i]), duration = .5)
            anim.start(self.robot)
            anim.bind(on_complete = partial(self.showMessage , message, listePos))
        else:
            self.showMessage(message, listePos)
    def showMessage(self, message, listePos, *args) :
        self.ids._labelResultat.text = message
        if len(listePos) >= 1:
            anim3= Animation(pos_hint = self.posToCoord(listePos[len(listePos) - 1]), duration =  2.5)
            anim3 += Animation(pos_hint =self.posToCoord(listePos[0]), duration = 0)
            anim3.start(self.robot)
    def posToCoord(self, pos) :
        return {"center_x" : (0.469040625 + ((pos%10 - 1) * 0.06328125)), "center_y": (0.10625 + ((8 - (pos//10)) * 0.1125))} # (x : début de l'image + demi case  + (unité de la pos * taille d'un carreau) y : début de l'image + demi carrreau +  dizaine de la pos * 9/8 * 0.1)
    def verif(self, texte):
        fichierLvl = open("assets/current_lvl.txt", "r")
        listePosition = []
        message = ""
        lvl = fichierLvl.read()
        texte = texte.lower()
        texteCoupe = texte.splitlines()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        if int(lvl) > len(Data) :
            message = "ERREUR : On a pas encore mis ce niveau"
        else :
            position = self.getOrigin(lvl)
            listePosition.append(position)
            orientation = 1
            nb = 0
            Terminer = False
            if "limite" in Data[int(lvl) - 1] :
                if len(texteCoupe) > Data[int(lvl) - 1]["limite"] :
                    Terminer = True
                    message = "ECHEC : Limite dépassée !"

            while not Terminer and nb != len(texteCoupe) :
                if texteCoupe[nb] == "avancer" :
                    position+= orientation
                elif texteCoupe[nb] == "droite" :
                    if orientation == 1 :
                        orientation = 10
                    elif orientation == 10 :
                        orientation = - 1
                    elif orientation == -1 :
                        orientation = - 10
                    elif orientation == -10 :
                        orientation = 1
                elif texteCoupe[nb] == "gauche" :
                    if orientation == 1 :
                        orientation = -10
                    elif orientation == 10 :
                        orientation = 1
                    elif orientation == -1 :
                        orientation = 10
                    elif orientation == -10 :
                        orientation = - 1
                elif texteCoupe[nb] == "reculer" :
                    position-= orientation
                elif texteCoupe[nb] == "attendre" and int(lvl) >= 9 :
                    pass
                elif texteCoupe[nb] == "sauter" and int(lvl) >= 9 :
                    if str((position) + orientation) in Data[int(lvl) - 1] :
                        message = "ECHEC : Tu ne peux sauter que le vide"
                        Terminer = True
                    else:
                        position += 2 * orientation

                else:
                    message = "ECHEC : Mot incorrect dans le script"
                    Terminer = True
                listePosition.append(position)
                if str(position) in Data[int(lvl) - 1] :
                    if Data[int(lvl) - 1][str(position)] == "c" or Data[int(lvl) - 1][str(position)] == "d" or Data[int(lvl) - 1][str(position)] == "f" :
                        pass
                    elif Data[int(lvl) - 1][str(position)] ==  "t-d" :
                        position += 1
                        listePosition.append(position)
                    elif Data[int(lvl) - 1][str(position)] ==  "t-g" :
                        position -= 1
                        listePosition.append(position)
                    elif Data[int(lvl) - 1][str(position)] ==  "t-h" :
                        position -= 10
                        listePosition.append(position)
                    elif Data[int(lvl) - 1][str(position)] ==  "t-b" :
                        position += 10
                        listePosition.append(position)
                    else:
                        message = "ERREUR : Faudrait corriger le json/le code"
                        Terminer = True
                else:
                    message = "ECHEC : Hors champs"
                    Terminer = True
                if str(position) in Data[int(lvl) - 1] :
                    if Data[int(lvl) - 1][str(position)] == "c" or Data[int(lvl) - 1][str(position)] == "d" or Data[int(lvl) - 1][str(position)] == "t-d" or Data[int(lvl) - 1][str(position)] == "t-g" or Data[int(lvl) - 1][str(position)] == "t-h" or Data[int(lvl) - 1][str(position)] == "t-b":
                        pass
                    elif Data[int(lvl) - 1][str(position)] == "f" :
                        if (nb + 1) == len(texteCoupe) :
                            message = "REUSSI : Bravo, tu as réussi le niveau " + lvl
                            self.changeLvlMax()
                            Terminer = True
                    else:
                        message = "ERREUR : Faudrait corriger le json/le code"
                        Terminer = True
                else:
                    message = "ECHEC : Hors champs"
                    Terminer = True
                nb +=1
            if not Terminer :
                message = "ECHEC : Il manque une/plusieurs instructions"
        return listePosition, message

class CoursScreen(Screen):
    pass

class CustomCoursScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class Incredibot(App):
    def build(self):
        self.title = 'Incredibot'
        self.icon = 'Images/icon.png'
        kv = Builder.load_file("main.kv")
        return kv
    def close_application(self):
        App.get_running_app().stop()
        Window.close()
if __name__ == "__main__":
    Config.set("input","mouse","mouse,multitouch_on_demand")
    Window.maximize()
    Incredibot().run()

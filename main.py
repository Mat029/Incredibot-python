""""
DOC PROVISOIRE !!!!

Voir ttes les recommandations précises dans readme sinon :

installer Kivy :
1) pip -m install kivy[base] dans votre terminal
2) Si votre éditeur le supporte (Pycharme/Thonny, Anaconda aussi je crois etc...) Vous pouvez installer directement kivy. Bien prendre le "grand" Kivy, avec toutes les dépendances.

ATTENTION IMPORTANT :

 1) Le code a été codé sur Python 3.9.10, et même si il devrait fonctionner sur python 3.7 (version de Thonny bundle), il "devrait". (Cf problème de migration vers 3.10 et patern dans readme)
 2) Un bug existait en 2.0.0 (et existe peut etre toujours en 2.1.0) et affectait nottament les pc de l'écoles, où kivy detecte une version d'open Gl qui n'est pas la bonne, ce qui provoque un crash. Dans ce cas, rajouter :
 import os
 os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.config import Config
import kivy
import json

kivy.require("2.1.0")

class HomeScreen(Screen):
    def cours(self):
        print("Bientôt disponible (normalement)")
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
            self.position = self.getOrigin(lvl)
            self.updateRobot()
            if "limite" in Data[int(lvl) - 1] :
                self.ids._labelInstruction.text = "Nombre max d'instructions : " + str(Data[int(lvl) - 1]["limite"])
            else:
                self.ids._labelInstruction.text = "Nombre max d'instructions : NAN"
        else:
            self.ids._imageRobot.pos_hint = {"center_x" : .2 , "center_y" : .5}
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
    def updateRobot(self) :
        self.ids._imageRobot.pos_hint = self.posToCoord() #La valeur change bien (g fait des test, ms le visuel s'update pas avant la fin de verif)
    def posToCoord(self) :
        return {"center_x" : (0.469040625 + ((self.position%10 - 1) * 0.06328125)), "center_y" : (0.10625 + ((8 - (self.position//10)) * 0.1125))} # (x : début de l'image + demi case  + (unité de la pos * taille d'un carreau) y : début de l'image + demi carrreau +  dizaine de la pos * 9/8 * 0.1)
    def verif(self, texte):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        texte = texte.lower()
        texteCoupe = texte.splitlines()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        if int(lvl) > len(Data) :
            self.showResult("ERREUR : On a pas encore mis ce niveau")
        else :
            self.position = self.getOrigin(lvl)
            orientation = 1
            nb = 0
            Terminer = False
            if "limite" in Data[int(lvl) - 1] :
                if len(texteCoupe) > Data[int(lvl) - 1]["limite"] :
                    Terminer = True
                    self.showResult("ECHEC : Limite dépassée !")

            while not Terminer and nb != len(texteCoupe) :
                if texteCoupe[nb] == "avancer" :
                    self.position+= orientation
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
                    self.position-= orientation
                else: 
                    self.showResult("ECHEC : Mot incorrect dans le script")
                    Terminer = True
                if str(self.position) in Data[int(lvl) - 1] :
                    if Data[int(lvl) - 1][str(self.position)] == "c" :
                        pass
                    elif Data[int(lvl) - 1][str(self.position)] == "d":
                        pass
                    elif Data[int(lvl) - 1][str(self.position)] == "f" :
                        if (nb + 1) == len(texteCoupe) :
                            self.showResult("REUSSI : Bravo, tu as réussi le niveau " + lvl) 
                            self.changeLvlMax()
                            Terminer = True
                    else: 
                        self.showResult("ERREUR : Faudrait corriger le json")
                        Terminer = True
                else: 
                    self.showResult("ECHEC : Hors champs")
                    Terminer = True
                nb +=1
            if not Terminer :
                self.showResult("ECHEC : Il manque une/plusieurs instructions")
            self.position = self.getOrigin(lvl)
    def showResult(self, resultat) :
        self.ids._labelResultat.text = resultat

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")

class Incredibot(App):
    def build(self):
        self.title = 'Incredibot'
        self.icon = 'Images/icon.png'
        return kv
    def close_application(self):
        App.get_running_app().stop()
        Window.close()
if __name__ == "__main__":
    Config.set("input","mouse","mouse,multitouch_on_demand")
    Window.maximize()
    Incredibot().run()
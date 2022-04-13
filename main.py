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
    def setLvl(self, lvl):
        fichier = open("assets/current_lvl.txt", "w")
        fichier.write(str(lvl))
        pass
    def getLvlMax(self):
        fichierMax = open("assets/max_level.txt", "r")
        lvlMax = fichierMax.read()
        return int(lvlMax)
    def getImage(self, lvl):
        lvlMax = self.getLvlMax()
        if lvlMax > lvl :
            return "Images/valide.png"
        elif lvlMax == lvl :
            return "Images/play.png"
        else:
            return "Images/cadenas.png"
    etage = 0
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
    def update(self):
        self.ids._Indicateur1.source = self.getImage((self.etage * 8 + 1))
        self.ids._Indicateur2.source = self.getImage((self.etage * 8 + 2))
        self.ids._Indicateur3.source = self.getImage((self.etage * 8 + 3))
        self.ids._Indicateur4.source = self.getImage((self.etage * 8 + 4))
        self.ids._Indicateur5.source = self.getImage((self.etage * 8 + 5))
        self.ids._Indicateur6.source = self.getImage((self.etage * 8 + 6))
        self.ids._Indicateur7.source = self.getImage((self.etage * 8 + 7))
        self.ids._Indicateur8.source = self.getImage((self.etage * 8 + 8))

class CustomLevelScreen(Screen):
    def chargement(self):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        fichierMax = open("assets/max_level.txt", "r")
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        lvlMax = fichierMax.read()
        self.ids._labelNomLvl.text = " Niveau " + lvl
        self.ids._buttonPrevious.disabled = int(lvl) == 1
        self.ids._buttonNext.disabled = int(lvlMax) <= int(lvl) or int(lvl) == 32
        self.ids._imageLvl.source = "Images/lvl/lvl" + lvl + ".png"
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
        self.ids._buttonCollecter.disabled = True
        self.ids._buttonCollecter.background_color = [0,0,0,0]
        self.ids._buttonCollecter.text = ""
        self.ids._buttonBoucle.disabled = True
        self.ids._buttonBoucle.background_color = [0,0,0,0]
        self.ids._buttonBoucle.text = ""
        if int(lvl) >= 9:
            self.ids._buttonSauter.disabled = False
            self.ids._buttonSauter.background_color = [1,1,1,1]
            self.ids._buttonSauter.text = "Sauter"
            self.ids._buttonAttendre.disabled = False
            self.ids._buttonAttendre.background_color = [1,1,1,1]
            self.ids._buttonAttendre.text = "Attendre"
        if int(lvl) >= 17:
            self.ids._buttonPrendre.disabled = False
            self.ids._buttonPrendre.background_color = [1,1,1,1]
            self.ids._buttonPrendre.text = "Prendre/Deposer"
        if int(lvl) >= 25:
            self.ids._buttonCollecter.disabled = False
            self.ids._buttonCollecter.background_color = [1,1,1,1]
            self.ids._buttonCollecter.text = "Collecter"
            self.ids._buttonBoucle.disabled = False
            self.ids._buttonBoucle.background_color = [1,1,1,1]
            self.ids._buttonBoucle.text = "Repeter X fois"
        posRobot = self.posToCoord(self.getOrigin(lvl))
        self.robot = Image(source = "Images/lvl/robot.png", size_hint =  [.050625 , .09],pos_hint = posRobot)
        self.ids._layoutLvl.add_widget(self.robot)
        if "limite" in Data[int(lvl) - 1] :
            self.ids._labelInstruction.text = "Instructions : 0 / " + str(Data[int(lvl) - 1]["limite"]) 
        else:
            self.ids._labelInstruction.text = "Instructions : 0 / ∞"
        if "nbObjet" in Data[int(lvl) - 1] :
            posObjet0 = self.posToCoord( Data[int(lvl) - 1]["dObjet0"])
            self.obj0 = Image(source = "Images/lvl/objet0.png", size_hint =  [.050625 , .09],pos_hint = posObjet0)
            self.ids._layoutLvl.add_widget(self.obj0)
            if Data[int(lvl) - 1]["nbObjet"] >= 2:
                posObjet1 = self.posToCoord( Data[int(lvl) - 1]["dObjet1"])
                self.obj1 = Image(source = "Images/lvl/objet1.png", size_hint =  [.050625 , .09],pos_hint = posObjet1)
                self.ids._layoutLvl.add_widget(self.obj1)
            if Data[int(lvl) - 1]["nbObjet"] == 3:
                posObjet2 = self.posToCoord( Data[int(lvl) - 1]["dObjet2"])
                self.obj2 = Image(source = "Images/lvl/objet2.png", size_hint =  [.050625 , .09],pos_hint = posObjet2)
                self.ids._layoutLvl.add_widget(self.obj2)
    def getLvl(self):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        return int(lvl)
    def setLvl(self, lvl):
        fichier = open("assets/current_lvl.txt", "w")
        fichier.write(str(lvl))
    def clean(self):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        Animation.cancel_all(self.robot)
        self.ids._layoutLvl.remove_widget(self.robot)
        if "nbObjet" in Data[int(lvl) - 1] :
            Animation.cancel_all(self.obj0)
            self.ids._layoutLvl.remove_widget(self.obj0)
            if Data[int(lvl) - 1]["nbObjet"] >= 2:
                Animation.cancel_all(self.obj1)
                self.ids._layoutLvl.remove_widget(self.obj1)
            if Data[int(lvl) - 1]["nbObjet"] == 3:
                Animation.cancel_all(self.obj2)
                self.ids._layoutLvl.remove_widget(self.obj2)
    def delLine(self, texte) :
        if texte!= "" :
            texteCoupe = texte.splitlines()
            del texteCoupe[-1]
            texte_final = "\n".join(texteCoupe)
            return (texte_final)
        else:
            return ""
    def prendreDeposer(self, texte):
        texte = texte.lower()
        texteCoupe = texte.splitlines()
        nbPrendre = 0
        nbDeposer = 0
        for i in texteCoupe :
            if i == "prendre" :
                nbPrendre +=1
        for j in texteCoupe:
            if j == "déposer" :
                nbDeposer += 1
        if nbPrendre > nbDeposer :
            return "\nDéposer"
        else:
            return "\nPrendre"
    def nbInstruction(self, texte):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        texteCoupe = texte.splitlines()
        limite = "∞"
        if "limite" in Data[int(lvl) - 1] :
            limite =  str(Data[int(lvl) - 1]["limite"])
            if len(texteCoupe) > Data[int(lvl) - 1]["limite"] :
                self.ids._labelInstruction.color = [1,0,0,1]
            else:
                self.ids._labelInstruction.color = [1,1,1,1]
        self.ids._labelInstruction.text = " Instructions : " + str(len(texteCoupe)) + " / " + limite
    def getOrigin(self, lvl) :
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        for i in Data[int(lvl) - 1] :
            if Data[int(lvl) - 1][i] == "d" :
                return int(i)
    def play(self, texte) :
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        listePos, listeObjet, message = self.verif(texte)
        Animation.stop_all(self.robot)
        anim = Animation(pos_hint =self.posToCoord(listePos[0]), duration = 0)
        if "nbObjet" in Data[int(lvl) - 1] :
            Animation.cancel_all(self.obj0)
            animObj0 = Animation(pos_hint =self.posToCoord(listeObjet[0][0]), duration = 0)
            if Data[int(lvl) - 1]["nbObjet"] >= 2:
                Animation.cancel_all(self.obj1)
                animObj1 = Animation(pos_hint =self.posToCoord(listeObjet[1][0]), duration = 0)
            if Data[int(lvl) - 1]["nbObjet"] == 3:
                Animation.cancel_all(self.obj2)
                animObj2 = Animation(pos_hint =self.posToCoord(listeObjet[2][0]), duration = 0)
        if len(listePos) >= 1 :
            for i in range(1, len(listePos)) :
                anim += Animation(pos_hint =self.posToCoord(listePos[i]), duration = .5)
        if "nbObjet" in Data[int(lvl) - 1] :
            for i in range(1, len(listeObjet[0])) :
                animObj0 += Animation(pos_hint =self.posToCoord(listeObjet[0][i]), duration = 0) #permet a l'objet d'apparaitre/disparaitre instant
                animObj0 += Animation(pos_hint =self.posToCoord(listeObjet[0][i]), duration = .5) 
                if Data[int(lvl) - 1]["nbObjet"] >= 2:
                    animObj1 += Animation(pos_hint =self.posToCoord(listeObjet[1][i]), duration = 0)
                    animObj1 += Animation(pos_hint =self.posToCoord(listeObjet[1][i]), duration = .5)
                if Data[int(lvl) - 1]["nbObjet"] == 3:
                    animObj2 += Animation(pos_hint =self.posToCoord(listeObjet[2][i]),duration = 0)
                    animObj2 += Animation(pos_hint =self.posToCoord(listeObjet[2][i]),duration = .5)
        anim.start(self.robot)
        anim.bind(on_complete = partial(self.showMessage , message, listePos, listeObjet))
        if "nbObjet" in Data[int(lvl) - 1] :
            animObj0.start(self.obj0)
            if Data[int(lvl) - 1]["nbObjet"] >= 2:
                animObj1.start(self.obj1)
            if Data[int(lvl) - 1]["nbObjet"] == 3:
                animObj2.start(self.obj2) 
    def showMessage(self, message, listePos, listePosObjet, *args) :
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        fichierMax = open("assets/max_level.txt", "r")
        lvlMax = fichierMax.read()
        self.ids._labelResultat.text = message
        self.ids._buttonNext.disabled = int(lvlMax) <= int(lvl) or int(lvl) == 32
        if len(listePos) >= 1:
            anim3= Animation(pos_hint = self.posToCoord(listePos[len(listePos) - 1]), duration =  2.5)
            anim3 += Animation(pos_hint =self.posToCoord(listePos[0]), duration = 0)
            anim3.start(self.robot)
        if "nbObjet" in Data[int(lvl) - 1] :
            anim4= Animation(pos_hint = self.posToCoord(listePosObjet[0][len(listePosObjet[0]) - 1]), duration =  2.5)
            anim4 += Animation(pos_hint =self.posToCoord(listePosObjet[0][0]), duration = 0)
            anim4.start(self.obj0)
            if Data[int(lvl) - 1]["nbObjet"] >= 2:
                anim5= Animation(pos_hint = self.posToCoord(listePosObjet[1][len(listePosObjet[1]) - 1]), duration =  2.5)
                anim5 += Animation(pos_hint =self.posToCoord(listePosObjet[1][0]), duration = 0)
                anim5.start(self.obj1)
            if Data[int(lvl) - 1]["nbObjet"] == 3:
                anim6= Animation(pos_hint = self.posToCoord(listePosObjet[2][len(listePosObjet[2]) - 1]), duration =  2.5)
                anim6 = Animation(pos_hint =self.posToCoord(listePosObjet[2][0]), duration = 0)
                anim6.start(self.obj2)
    def posToCoord(self, pos) :
        return {"center_x" : (0.455625 + 0.0333984375 + ((pos%10 - 1) * 0.066796875)), "center_y": (0.025 + 0.059375 + ((8 - (pos//10)) * 0.11875))} # (x : début de l'image + demi case  + (unité de la pos * taille d'un carreau) y : début de l'image + demi carrreau +  dizaine de la pos * 9/8 * 0.1)
    def verif(self, texte):
        fichierLvl = open("assets/current_lvl.txt", "r")
        listePosition = []
        message = ""
        lvl = fichierLvl.read()
        texte = texte.lower()
        texteCoupe = texte.splitlines()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        position = self.getOrigin(lvl)
        listePosition.append(position)
        orientation = 1
        nb = 0
        Terminer = False
        posObjet = [0,0,0]
        listeObjet = [[],[],[]]
        objet = 3
        tenirObjet = False
        if "nbObjet" in Data[int(lvl) - 1] :
            for p in range(Data[int(lvl) - 1]["nbObjet"]) :
                posObjet[p] = Data[int(lvl) - 1]["dObjet" + str(p)]
                listeObjet[p].append(posObjet[p])
        if "limite" in Data[int(lvl) - 1] :
            if len(texteCoupe) > Data[int(lvl) - 1]["limite"] :
                Terminer = True
                message = "ECHEC : Limite dépassée !"
        elif len(texteCoupe) > 100 :
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
            elif texteCoupe[nb] == "prendre" and int(lvl) >= 17 :
                if not tenirObjet :
                    i = 0
                    while i < len(posObjet) and not tenirObjet:
                        if posObjet[i] == (position + orientation) :
                            objet = i
                            posObjet[objet] = 0
                            tenirObjet = True
                            i +=1
                else:
                    message = "ECHEC : Tu tiens déja un objet"
                    Terminer = True
            elif texteCoupe[nb] == "déposer" and int(lvl) >= 17 :
                if tenirObjet:
                    if (Data[int(lvl) - 1][(str(position + orientation))] == "c" or Data[int(lvl) - 1][str(position + orientation)] == "d" or Data[int(lvl) - 1][str(position + orientation)] == "f") and (position + orientation) not in posObjet:
                        posObjet[objet] = (position + orientation)
                    else:
                        message = "ECHEC : Tu ne peux pas poser un objet ici"
                        Terminer = True
                else:
                    message = "ECHEC : Tu ne tiens pas d'objet"
                    Terminer = True


                

            else:
                message = "ECHEC : Mot incorrect dans le script"
                Terminer = True
            listePosition.append(position)
            if "nbObjet" in Data[int(lvl) - 1] :
                for p in range(Data[int(lvl) - 1]["nbObjet"]) :
                    listeObjet[p].append(posObjet[p])
            if str(position) in Data[int(lvl) - 1] :
                if Data[int(lvl) - 1][str(position)] == "c" or Data[int(lvl) - 1][str(position)] == "d" or Data[int(lvl) - 1][str(position)] == "f" :
                    pass
                elif Data[int(lvl) - 1][str(position)] ==  "t-d" :
                    position += 1
                    listePosition.append(position)
                    if "nbObjet" in Data[int(lvl) - 1] :
                        for p in range(Data[int(lvl) - 1]["nbObjet"]) :
                            listeObjet[p].append(posObjet[p])                 
                elif Data[int(lvl) - 1][str(position)] ==  "t-g" :
                    position -= 1
                    if "nbObjet" in Data[int(lvl) - 1] :
                        for p in range(Data[int(lvl) - 1]["nbObjet"]) :
                            listeObjet[p].append(posObjet[p])
                    listePosition.append(position)
                elif Data[int(lvl) - 1][str(position)] ==  "t-h" :
                    position -= 10
                    if "nbObjet" in Data[int(lvl) - 1] :
                        for p in range(Data[int(lvl) - 1]["nbObjet"]) :
                            listeObjet[p].append(posObjet[p])
                    listePosition.append(position)
                elif Data[int(lvl) - 1][str(position)] ==  "t-b" :
                    if "nbObjet" in Data[int(lvl) - 1] :
                        for p in range(Data[int(lvl) - 1]["nbObjet"]) :
                            listeObjet[p].append(posObjet[p])
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
                        fini = True
                        if "nbObjet" in Data[int(lvl) - 1] :
                            i = 0
                            while i < Data[int(lvl) - 1]["nbObjet"] and fini:
                                fini = posObjet[i] == Data[int(lvl) - 1]["fObjet" + str(i)]
                                i+=1
                        if fini :
                            message = "REUSSI : Bravo, tu as réussi le niveau " + lvl
                            fichierMax = open("assets/max_level.txt", "r+")
                            if (int(lvl) +1) > int(fichierMax.read()):
                                fichierMax.seek(0)
                                fichierMax.truncate()
                                fichierMax.write(str(int(lvl) +1))
                        else:
                            message = "ECHEC : Un objet n'est pas à sa place "
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
        return listePosition, listeObjet, message
    
    def indice(self):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        if "indice" in Data[int(lvl) - 1] :
            self.ids._labelResultat.text = Data[int(lvl) - 1]["indice"]
        else:
            self.ids._labelResultat.text = "Pas d'indice pour ce niveau"

        
    def cancel(self) :
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        Animation.cancel_all(self.robot)
        self.robot.pos_hint = self.posToCoord(self.getOrigin(lvl))
        

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

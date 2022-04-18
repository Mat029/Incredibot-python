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
        fichierMax.close()
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
        self.update()
    def baisse(self):
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
        self.ids._imageAugmente.source = 'Images/icon/next_icon.png' if (self.etage != 2) else 'Images/icon/next_icon_dark.png'
        self.ids._imageBaisse.source = 'Images/icon/previous_icon.png' if (self.etage != 0) else 'Images/icon/previous_icon_dark.png'

class CustomLevelScreen(Screen):
    def chargement(self):
        lvl = self.getLvl()
        fichierMax = open("assets/max_level.txt", "r")
        lvlMax = fichierMax.read()
        fichierMax.close()
        DataLvl = self.getLvlJson()
        self.ids._labelNomLvl.text = " Niveau " + str(lvl)
        self.ids._buttonPrevious.disabled = lvl == 1
        self.ids._buttonNext.disabled = int(lvlMax) <= lvl or lvl == 24
        self.ids._imageLvl.source = "Images/lvl/lvl" + str(lvl) + ".png"
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
        if lvl >= 25:
            self.ids._buttonCollecter.disabled = False
            self.ids._buttonCollecter.background_color = [1,1,1,1]
            self.ids._buttonCollecter.text = "Collecter"
            self.ids._buttonBoucle.disabled = False
            self.ids._buttonBoucle.background_color = [1,1,1,1]
            self.ids._buttonBoucle.text = "Repeter X fois"
        posRobot = self.posToCoord(DataLvl["d"])
        self.robot = Image(source = "Images/lvl/robot.png", size_hint =  [.066796875 , .11875],pos_hint = posRobot)
        self.ids._layoutLvl.add_widget(self.robot)
        if "limite" in DataLvl :
            self.ids._labelInstruction.text = "Instructions : 0 / " + str(DataLvl["limite"]) 
        else:
            self.ids._labelInstruction.text = "Instructions : 0 / ∞"
        if "nbObjets" in DataLvl :
            posObjet0 = self.posToCoord( DataLvl["dObjet0"])
            self.obj0 = Image(source = "Images/lvl/objet0.png", size_hint =  [.066796875 , .11875],pos_hint = posObjet0, allow_stretch = True)
            self.ids._layoutLvl.add_widget(self.obj0)
            if DataLvl["nbObjets"] >= 2:
                posObjet1 = self.posToCoord( DataLvl["dObjet1"])
                self.obj1 = Image(source = "Images/lvl/objet1.png", size_hint =  [.066796875 , .11875],pos_hint = posObjet1, allow_stretch = True)
                self.ids._layoutLvl.add_widget(self.obj1)
            if DataLvl["nbObjets"] == 3:
                posObjet2 = self.posToCoord( DataLvl["dObjet2"])
                self.obj2 = Image(source = "Images/lvl/objet2.png", size_hint =  [.066796875 , .11875],pos_hint = posObjet2, allow_stretch = True)
                self.ids._layoutLvl.add_widget(self.obj2)

    def getLvl(self):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        fichierLvl.close
        return int(lvl)

    def getLvlJson(self) :
        lvl = self.getLvl()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        MyJson.close()
        DataLvl = Data[lvl - 1]
        return DataLvl

    def setLvl(self, lvl):
        fichier = open("assets/current_lvl.txt", "w")
        fichier.write(str(lvl))
        fichier.close()

    def clean(self):
        DataLvl = self.getLvlJson()
        Animation.cancel_all(self.robot)
        self.ids._layoutLvl.remove_widget(self.robot)
        if "nbObjets" in DataLvl :
            Animation.cancel_all(self.obj0)
            self.ids._layoutLvl.remove_widget(self.obj0)
            if DataLvl["nbObjets"] >= 2:
                Animation.cancel_all(self.obj1)
                self.ids._layoutLvl.remove_widget(self.obj1)
            if DataLvl["nbObjets"] == 3:
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
        DataLvl = self.getLvlJson()
        texteCoupe = texte.splitlines()
        limite = "∞"
        if "limite" in DataLvl :
            limite =  str(DataLvl["limite"])
            if len(texteCoupe) > DataLvl["limite"] :
                self.ids._labelInstruction.color = [1,0,0,1]
            else:
                self.ids._labelInstruction.color = [1,1,1,1]
        self.ids._labelInstruction.text = " Instructions : " + str(len(texteCoupe)) + " / " + limite
    def play(self, texte) :
        DataLvl = self.getLvlJson()
        listePos, listeObjet, message = self.verif(texte)
        print(listeObjet)
        Animation.stop_all(self.robot)
        anim = Animation(pos_hint =self.posToCoord(listePos[0]), duration = 0)
        if "nbObjets" in DataLvl :
            Animation.cancel_all(self.obj0)
            animObj0 = Animation(pos_hint =self.posToCoord(listeObjet[0][0]), duration = 0)
            if DataLvl["nbObjets"] >= 2:
                Animation.cancel_all(self.obj1)
                animObj1 = Animation(pos_hint =self.posToCoord(listeObjet[1][0]), duration = 0)
            if DataLvl["nbObjets"] == 3:
                Animation.cancel_all(self.obj2)
                animObj2 = Animation(pos_hint =self.posToCoord(listeObjet[2][0]), duration = 0)
        if len(listePos) >= 1 :
            for i in range(1, len(listePos)) :
                anim += Animation(pos_hint =self.posToCoord(listePos[i]), duration = .5)
        if "nbObjets" in DataLvl :
            for i in range(1, len(listeObjet[0])) :
                animObj0 += Animation(pos_hint =self.posToCoord(listeObjet[0][i]), duration = 0) #permet a l'objet d'apparaitre/disparaitre instant
                animObj0 += Animation(pos_hint =self.posToCoord(listeObjet[0][i]), duration = .5) 
                if DataLvl["nbObjets"] >= 2:
                    animObj1 += Animation(pos_hint =self.posToCoord(listeObjet[1][i]), duration = 0)
                    animObj1 += Animation(pos_hint =self.posToCoord(listeObjet[1][i]), duration = .5)
                if DataLvl["nbObjets"] == 3:
                    animObj2 += Animation(pos_hint =self.posToCoord(listeObjet[2][i]),duration = 0)
                    animObj2 += Animation(pos_hint =self.posToCoord(listeObjet[2][i]),duration = .5)
        anim.start(self.robot)
        anim.bind(on_complete = partial(self.finAnim , message, listePos, listeObjet))
        if "nbObjets" in DataLvl :
            animObj0.start(self.obj0)
            if DataLvl["nbObjets"] >= 2:
                animObj1.start(self.obj1)
            if DataLvl["nbObjets"] == 3:
                animObj2.start(self.obj2) 
    def finAnim(self, message, listePos, listePosObjet, *args) :
        lvl = self.getLvl()
        DataLvl = self.getLvlJson()
        fichierMax = open("assets/max_level.txt", "r")
        lvlMax = fichierMax.read()
        fichierMax.close()
        self.ids._labelResultat.text = message
        self.ids._buttonNext.disabled = int(lvlMax) <= lvl or lvl == 24
        if len(listePos) >= 1:
            anim3= Animation(pos_hint = self.posToCoord(listePos[len(listePos) - 1]), duration =  2.5)
            anim3 += Animation(pos_hint =self.posToCoord(listePos[0]), duration = 0)
            anim3.start(self.robot)
        if "nbObjets" in DataLvl :
            anim4= Animation(pos_hint = self.posToCoord(listePosObjet[0][len(listePosObjet[0]) - 1]), duration =  2.5)
            anim4 += Animation(pos_hint =self.posToCoord(listePosObjet[0][0]), duration = 0)
            anim4.start(self.obj0)
            if DataLvl["nbObjets"] >= 2:
                anim5= Animation(pos_hint = self.posToCoord(listePosObjet[1][len(listePosObjet[1]) - 1]), duration =  2.5)
                anim5 += Animation(pos_hint =self.posToCoord(listePosObjet[1][0]), duration = 0)
                anim5.start(self.obj1)
            if DataLvl["nbObjets"] == 3:
                anim6= Animation(pos_hint = self.posToCoord(listePosObjet[2][len(listePosObjet[2]) - 1]), duration =  2.5)
                anim6 += Animation(pos_hint =self.posToCoord(listePosObjet[2][0]), duration = 0)
                anim6.start(self.obj2)
    def posToCoord(self, pos) :
        return {"center_x" : (0.455625 + 0.0333984375 + ((pos%10 - 1) * 0.066796875)), "center_y": (0.025 + 0.059375 + ((8 - (pos//10)) * 0.11875))} # (x : début de l'image + demi case  + (unité de la pos * taille d'un carreau) y : début de l'image + demi carrreau +  dizaine de la pos * 9/8 * 0.1)
    def verif(self,texte) :
        lvl = self.getLvl()
        DataLvl = self.getLvlJson()
        texte = texte.lower()
        listeInstructions = texte.splitlines()
        listePosRobot = []
        listePosObjets = []
        posObjets = []
        message = "ECHEC : Il manque une/des instruction(s)"
        posRobot = DataLvl["d"]
        listePosRobot.append(posRobot)
        orientationRobot = 1
        cyleOrientation = { 1 : 10, 10 : -1, -1 : -10, -10 : 1} # Permet de changer l'orientation sans avoir à faire 40 milles if/elif (gain de perfs), initialement orienté pour tourner à droite
        cycleTapis = {"t-d" : 1, "t-g" : -1, "t-h" : -10, "t-b" : 10}
        if "nbObjets" in DataLvl : 
            posObjets = [DataLvl["dObjet" + str(s)] for s in range(DataLvl["nbObjets"])]
            listePosObjets = [[s] for s in posObjets]
            objet = {"tenir" : False, "numero" : 0}
        terminer = ("limite" in DataLvl and DataLvl["limite"] < len(listeInstructions) or (len(listeInstructions) > 100))
        if terminer :
            message = "ECHEC : Limite d'instructions dépassé"
        nbExecution = 0
        while not terminer and nbExecution < len(listeInstructions) :
            instruction = listeInstructions[nbExecution]
            if instruction == "avancer" :
                posRobot += orientationRobot
            elif instruction == "reculer" :
                posRobot -= orientationRobot
            elif instruction == "droite" :
                orientationRobot = cyleOrientation[orientationRobot]
            elif instruction == "gauche" :
                orientationRobot = - cyleOrientation[orientationRobot]
            elif instruction == "attendre" and lvl >= 9 :
                pass
            elif instruction == "sauter" and lvl >= 9 :
                if str(posRobot + orientationRobot) in DataLvl :
                    terminer = True
                    message = "ECHEC : Tu ne peut sauter que par dessus le vide"
                else :
                    posRobot += 2 * orientationRobot
            elif instruction == "prendre" and lvl >= 17 :
                if "nbObjets" in DataLvl and (posRobot + orientationRobot) in posObjets:
                    if objet["tenir"] :
                        terminer = True
                        message = "ECHEC : Tu tiens déjà un objet"
                    else: 
                        objet["tenir"] = True
                        objet["numero"] = posObjets.index((posRobot + orientationRobot))
                        posObjets[objet["numero"]] = 0
                else :
                    terminer = True
                    message = "ECHEC : Il n'y a pas d'objet à prendre"
            elif instruction == "déposer" and lvl >= 17 :
                if "nbObjets" in DataLvl and objet["tenir"] :
                    if str(posRobot + orientationRobot) in DataLvl and DataLvl[str(posRobot + orientationRobot)] in ["c","f"] and (posRobot + orientationRobot) not in posObjets :
                        objet["tenir"] = False
                        posObjets[objet["numero"]] = posRobot + orientationRobot
                    else:
                        terminer = True
                        message = "ECHEC : Tu ne peux pas poser d'objet ici"
                else:
                    terminer = True
                    message = "ECHEC : Tu n'as pas d'objet à poser"
            else :
                terminer = True
                message = "ECHEC : Mot incorrect dans le script"
            listePosRobot.append(posRobot)
            for c in range(len(listePosObjets)) :
                listePosObjets[c].append(posObjets[c])
            if str(posRobot) in DataLvl :
                if "tp" in DataLvl[str(posRobot)] :
                    posRobot = int(DataLvl[str(posRobot)][-2:])
                    listePosRobot.append(posRobot)
                    for c in range(len(listePosObjets)) :
                        listePosObjets[c].append(posObjets[c])
                elif "t-" in DataLvl[str(posRobot)] :
                    posRobot += cycleTapis[DataLvl[str(posRobot)]]
                    listePosRobot.append(posRobot)
                    for c in range(len(listePosObjets)) :
                        listePosObjets[c].append(posObjets[c])  #(nécessaire pour que les anims des objets et du robot soit synchro)
                if str(posRobot) in DataLvl :
                    if not (posRobot in posObjets) :
                        if DataLvl[str(posRobot)] == "f" and (nbExecution +1) == len(listeInstructions) :
                            terminer = True
                            succes = True
                            nbObjets = len(posObjets)
                            while succes and nbObjets > 0 :
                                succes = (posObjets[nbObjets - 1] == DataLvl["fObjet" + str(nbObjets - 1)]) 
                                nbObjets -=1
                            if succes :
                                message = "REUSSI : Bravo, tu as réussi le niveau " + str(lvl)
                                fichierMax = open("assets/max_level.txt", "r+")
                                if (lvl +1) > int(fichierMax.read()):
                                    fichierMax.seek(0)
                                    fichierMax.truncate()
                                    fichierMax.write(str(lvl +1))
                                fichierMax.close
                            else :
                                message = "ECHEC : Un objet n'est pas à sa place "
                    else :
                        terminer = True
                        message = "ECHEC : Tu ne peux pas traverser un objet"
                else: 
                    terminer = True
                    message = "ECHEC : Tu sors du parcours"
            else :
                terminer = True
                message = "ECHEC : Tu sors du parcours"
            nbExecution += 1
        return listePosRobot, listePosObjets, message
    
    def indice(self):
        DataLvl = self.getLvlJson()
        if "indice" in DataLvl :
            self.ids._labelResultat.text = DataLvl["indice"]
        else:
            self.ids._labelResultat.text = "Pas d'indice pour ce niveau"
        
    def cancel(self) :
        DataLvl = self.getLvlJson()
        Animation.cancel_all(self.robot)
        self.robot.pos_hint = self.posToCoord(DataLvl["d"])
        if "nbObjets" in DataLvl :
            Animation.cancel_all(self.obj0)
            self.obj0.pos_hint = self.posToCoord( DataLvl["dObjet0"])
            if DataLvl["nbObjets"] >=2 :
                Animation.cancel_all(self.obj1)
                self.obj1.pos_hint = self.posToCoord( DataLvl["dObjet1"])
                if DataLvl["nbObjets"] == 3 :
                    Animation.cancel_all(self.obj2)
                    self.obj2.pos_hint = self.posToCoord( DataLvl["dObjet2"])
        

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

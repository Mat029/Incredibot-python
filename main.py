from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import json

class HomeScreen(Screen):
    def cours(self):
        print("tkt ça vient")
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
        self.ids._boutonAugmente.disabled = (self.etage == 7)
        self.ids._boutonBaisse.disabled = (self.etage == 0)
        self.ids._labelEtage.text = str(self.etage +1)
        self.ids._bouton1.text = "Stage " + str(self.etage * 8 + 1)
        self.ids._bouton2.text = "Stage " + str(self.etage * 8 + 2)
        self.ids._bouton3.text = "Stage " + str(self.etage * 8 + 3)
        self.ids._bouton4.text = "Stage " + str(self.etage * 8 + 4)
        self.ids._bouton5.text = "Stage " + str(self.etage * 8 + 5)
        self.ids._bouton6.text = "Stage " + str(self.etage * 8 + 6)
        self.ids._bouton7.text = "Stage " + str(self.etage * 8 + 7)
        self.ids._bouton8.text = "Stage " + str(self.etage * 8 + 8)
        self.update()
    def baisse(self):
        self.etage-=1
        self.ids._boutonAugmente.disabled = (self.etage == 7)
        self.ids._boutonBaisse.disabled = (self.etage == 0)
        self.ids._labelEtage.text = str(self.etage +1)
        self.ids._bouton1.text = "Stage " + str(self.etage * 8 + 1)
        self.ids._bouton2.text = "Stage " + str(self.etage * 8 + 2)
        self.ids._bouton3.text = "Stage " + str(self.etage * 8 + 3)
        self.ids._bouton4.text = "Stage " + str(self.etage * 8 + 4)
        self.ids._bouton5.text = "Stage " + str(self.etage * 8 + 5)
        self.ids._bouton6.text = "Stage " + str(self.etage * 8 + 6)
        self.ids._bouton7.text = "Stage " + str(self.etage * 8 + 7)
        self.ids._bouton8.text = "Stage " + str(self.etage * 8 + 8) 
        self.update()
    pass

class CustomLevelScreen(Screen):
    def chargement(self):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        self.ids._labelNomLvl.text = "[b]Niveau " + lvl + "[/b]"
        self.ids._imageLvl.source = "Images/lvl/lvl" + lvl + ".png"
        self.ids._labelResultat.text = ""
        self.ids._userInput.text = ""
    def changeLvlMax(self):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        fichierMax = open("assets/max_level.txt", "r+")
        if (int(lvl) +1) > int(fichierMax.read()):
            fichierMax.seek(0) 
            fichierMax.truncate() 
            fichierMax.write(str(int(lvl) +1))
    def verif(self, texte):
        fichierLvl = open("assets/current_lvl.txt", "r")
        lvl = fichierLvl.read()
        texte = texte.lower()
        texteCoupe = texte.splitlines()
        MyJson = open('assets/data.json',)
        Data = json.load(MyJson)
        pos = 0
        nb = 0
        orientation = 1
        Terminer = False
        if int(lvl) > len(Data) :
            self.showResult("ERREUR : On a pas encore mis ces assets la")
        else :
            for i in Data[int(lvl) - 1] :
                if Data[int(lvl) - 1][i] == "d" :
                    pos = int(i)
            while not Terminer and nb != len(texteCoupe) :
                if texteCoupe[nb] == "avancer" :
                    pos+= orientation
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
                    pos-= orientation
                else: 
                    self.showResult("ECHEC : apprends à écrire bouffon(e)")
                    Terminer = True
                if str(pos) in Data[int(lvl) - 1] :
                    if Data[int(lvl) - 1][str(pos)] == "c" :
                        pass
                    elif Data[int(lvl) - 1][str(pos)] == "d":
                        pass
                    elif Data[int(lvl) - 1][str(pos)] == "f" :
                        if (nb + 1) == len(texteCoupe) :
                            self.showResult("REUSSI : t'enflamme pas c juste le lvl " + lvl)
                            self.changeLvlMax()
                            Terminer = True
                        else: 
                            self.showResult("ECHEC : Trop d'instruction vrmt, où est passé le pouvoir de la flemme ?")
                            Terminer = True
                    else: 
                        self.showResult("ERREUR : Faudrait corriger le json")
                        Terminer = True
                else: 
                    self.showResult("ECHEC : hors champs")
                    Terminer = True
                nb +=1
            if not Terminer :
                self.showResult("ECHEC : ça manque d'instruction ton bail")
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
    Window.maximize()
    Incredibot().run()
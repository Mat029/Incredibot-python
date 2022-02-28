from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.core.window import Window

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
        fichier = open("current_lvl.txt", "w")
        fichier.write(str(lvl)) 
        pass
    def getLvlMax(self):
        fichierMax = open("max_level.txt", "r")
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
        fichierLvl = open("current_lvl.txt", "r")
        self.ids._labelNomLvl.text = "Niveau " + fichierLvl.read()
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")

class Incredibot(App):
    def changeLvlMax(self):
        fichierActuel = open("current_lvl.txt", "r")
        lvl = fichierActuel.read()
        fichierMax = open("max_level.txt", "r+")
        if (int(lvl) +1) > int(fichierMax.read()):
            fichierMax.seek(0) 
            fichierMax.truncate() 
            fichierMax.write(str(int(lvl) +1))
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
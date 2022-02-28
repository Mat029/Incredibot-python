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
    def setLvl(self, lvl):
        fichier = open("current_lvl.txt", "w")
        fichier.write(str(lvl)) 
        pass
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
    pass

class Level_1(Screen):
    pass

class Level_2(Screen):
    pass

class Level_3(Screen):
    pass

class Level_4(Screen):
    pass

class Level_5(Screen):
    pass

class Level_6(Screen):
    pass

class Level_7(Screen):
    pass

class Level_8(Screen):
    pass

class Level_9(Screen):
    pass

class Level_10(Screen):
    pass

class Level_11(Screen):
    pass

class Level_12(Screen):
    pass

class Level_13(Screen):
    pass

class Level_14(Screen):
    pass

class Level_15(Screen):
    pass

class Level_16(Screen):
    pass

class Level_17(Screen):
    pass

class Level_18(Screen):
    pass

class Level_19(Screen):
    pass

class Level_20(Screen):
    pass

class Level_21(Screen):
    pass

class Level_22(Screen):
    pass

class Level_23(Screen):
    pass

class Level_24(Screen):
    pass

class Level_25(Screen):
    pass

class Level_26(Screen):
    pass

class Level_27(Screen):
    pass

class Level_28(Screen):
    pass

class Level_29(Screen):
    pass

class Level_30(Screen):
    pass

class Level_31(Screen):
    pass

class Level_32(Screen):
    pass

class Level_33(Screen):
    pass

class Level_34(Screen):
    pass

class Level_35(Screen):
    pass

class Level_36(Screen):
    pass

class Level_37(Screen):
    pass

class Level_38(Screen):
    pass

class Level_39(Screen):
    pass

class Level_40(Screen):
    pass

class Level_41(Screen):
    pass

class Level_42(Screen):
    pass

class Level_43(Screen):
    pass

class Level_44(Screen):
    pass

class Level_45(Screen):
    pass

class Level_46(Screen):
    pass

class Level_47(Screen):
    pass

class Level_48(Screen):
    pass

class Level_49(Screen):
    pass

class Level_50(Screen):
    pass

class Level_51(Screen):
    pass

class Level_52(Screen):
    pass

class Level_53(Screen):
    pass

class Level_54(Screen):
    pass

class Level_55(Screen):
    pass

class Level_56(Screen):
    pass

class Level_57(Screen):
    pass

class Level_58(Screen):
    pass

class Level_59(Screen):
    pass

class Level_60(Screen):
    pass

class Level_61(Screen):
    pass

class Level_62(Screen):
    pass

class Level_63(Screen):
    pass

class Level_64(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")

class AppPasMain(App):
    def getLvlMax(self):
        fichierMax = open("max_level.txt", "r")
        lvlMax = fichierMax.read()
        return lvlMax
    def changeLvlMax(self):
        fichierActuel = open("current_lvl.txt", "r")
        lvl = fichierActuel.read()
        fichierMax = open("max_level.txt", "r+")
        if str(int(lvl) +1) > fichierMax.read():
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
    AppPasMain().run()
import pyxel
from random import randint

size = 128


class Glass:
   
    def  __init__(self):
        self.run = True
        self.height= randint(30,50)
        self.w=randint(15,40)
        self.volume_total=self.w*self.w*self.height
        self.volume = 0
        self.y=size//1.35 - self.height//2
        self.x=size//2 - self.w//2
        self.point = self.y+self.height
        self.voulu = randint(30,90)/100
        self.volume_mousse_final = 0
        self.moussing = False
        self.volume_mousse = 0
    def get_voulume_mousse(self):
        self.volume_mousse_final = int(randint(20,70)/100 *self.volume)
    def draw(self):
        # affiche le niveau d'alcool
        self.point = int(self.y + self.height - self.height * self.pourcent_calcul())
        pyxel.rect(self.x,self.point,self.w,self.y + self.height-self.point,10)

        # affiche le niveau de mousse
        point_mousse = int(self.point - self.height*self.pourcent_mousse_calcul())
        pyxel.rect(self.x,point_mousse,self.w,self.point-point_mousse,7)
        
        # limite
        self.point = int(self.y + self.height - self.height * self.voulu)
        pyxel.line(self.x,self.point,self.x+self.w,self.point,13)

        """
        # limit ex
        self.point = int(self.y + self.height - self.height * (self.voulu-0.05))
        pyxel.line(self.x, self.point, self.x + self.w, self.point, 9)

        self.point = int(self.y + self.height - self.height * (self.voulu + 0.05))
        pyxel.line(self.x, self.point, self.x + self.w, self.point, 9)

        self.point = int(self.y + self.height - self.height * (self.voulu - 0.1))
        pyxel.line(self.x, self.point, self.x + self.w, self.point, 11)

        self.point = int(self.y + self.height - self.height * (self.voulu + 0.1))
        pyxel.line(self.x, self.point, self.x + self.w, self.point, 11)
        """
        
        # dessine le verre
        pyxel.line(self.x,self.y, self.x,self.y+self.height, 0)
        pyxel.line(self.x,self.y+self.height, self.x+self.w,self.y+self.height, 0)
        pyxel.line(self.x+self.w,self.y+self.height, self.x+self.w,self.y, 0)
    def pourcent_calcul_total(self):
        return (self.volume + self.volume_mousse) / self.volume_total
    def pourcent_calcul(self):
        return self.volume / self.volume_total

    def pourcent_mousse_calcul(self):
        return self.volume_mousse / self.volume_total

class Robinet:
    def __init__(self):
        self.debit = 250

class App:
    def __init__(self):

        self.scorre = 0
        self.timer = None
        self.txt = None
        pyxel.init(size,size)
        pyxel.load("my_resource.pyxres")
        self.verre = Glass()
        self.rob = Robinet()
        self.menu = True
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.menu:

            if self.verre.run:
                if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)  :

                    self.verre.get_voulume_mousse()
                    self.verre.run = False
                    self.verre.moussing = True

                self.verre.volume += self.rob.debit

            else:
                if self.verre.moussing:
                    if self.verre.volume_mousse_final > self.verre.volume_mousse:
                        self.verre.volume_mousse += 200
                        if self.verre.pourcent_calcul_total() > 1:
                            self.verre.moussing = False
                            self.timer = pyxel.frame_count
                            self.scorre += self.get_points(abs(self.verre.voulu - self.verre.pourcent_calcul_total()))
                    else:
                        self.verre.moussing = False
                        self.timer = pyxel.frame_count
                        self.scorre += self.get_points(abs(self.verre.voulu - self.verre.pourcent_calcul_total()))

                elif  self.timer + 60 < pyxel.frame_count:

                    self.verre = Glass()
                    self.txt = None


            if self.verre.pourcent_calcul() > 1:
                self.menu = True
        else:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)  :
                self.menu = False
                self.verre = Glass()

    
    def draw(self):
        if self.menu:
            pyxel.cls(pyxel.COLOR_CYAN)
            pyxel.text(16,48,"Press Space or button",0)

        else:
            pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
            if self.verre.run:
                pyxel.rect(64,40,8,self.verre.y+self.verre.height-40,10)
            if self.txt is not None:
                pyxel.text(48,48,self.txt,0)
            self.verre.draw()
            pyxel.text(16,16,str(self.scorre),0)

    def get_points(self,delta):

        if delta < 0.05:
            self.txt = "exelent"
            return 10
        if delta < 0.1:
            self.txt = "good job"
            return 5
        if delta < 0.3:
            self.txt = "null"
            return -2
        return 0
    
App()
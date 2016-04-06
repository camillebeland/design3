from maestroControl import maestro

# classe permettant de controller la camera sur deux axes de rotation.
# le servomoteur du haut (self.VERTical) doit etre branche sur le
# 5e port du pololu, le servomoteur du bas (self.HORizontal) doit etre
# branche sur le 4e port


class CameraRotationControl:
    def __init__(self, usb):
        self.MIDDLE = 6000
        VERT_MAX = 6000
        VERT_MIN = 2500
        HOR_MAX = 10000
        HOR_MIN = 2000
        self.HOR = 4
        self.VERT = 5
        self.controller = maestro.Controller(usb)
        self.setVertSpeed()
        self.setHorSpeed()
        self.controller.setRange(self.HOR, HOR_MIN, HOR_MAX)
        self.controller.setRange(self.VERT, VERT_MIN, VERT_MAX)
        self.sleep()
    
    #position de repos
    def sleep(self):
        self.controller.setTarget(self.HOR, self.MIDDLE)
        self.controller.setTarget(self.VERT, self.MIDDLE)

    #methode permettant de definir la potition horizontale de la camera
    #units: position on unites, de -1000 a 1000
    def setHor(self, units):
        target = (units*4) + 6000
        self.controller.setTarget(self.HOR, target)

    #methode permettant de definir la potition horizontale de la camera
    #units: position en units, de 0 a 1000
    def setVert(self, units):
        target = int(units*3.5) + 2500
        self.controller.setTarget(self.VERT, target)

    #methode permettant de bouger la camera d'un nombre d'unites. 
    #de -2000 a 2000
    def moveHor(self, units):
        currentPos = self.controller.getPosition(self.HOR)
        target = currentPos + (units*4)
        self.controller.setTarget(self.HOR, target)


    #methode permettant de bouger la camera d'un nombre d'unites. 
    #de -2000 a 2000
    def moveVert(self, units):
        currentPos = self.controller.getPosition(self.VERT)
        target = currentPos + (units*3.5)
        self.controller.setTarget(self.VERT, target)

    #methode permettant de definir une vitesse de transition
    # 0 = max speed
    # 1 = min speed (1 minute pour rotation complete)
    # 60 = 1 seconde pour rotation complete
    def setHorSpeed(self, speed = 0):
        self.controller.setSpeed(self.HOR, speed)


    #methode permettant de definir une vitesse de transition
    # 0 = max speed
    # 1 = min speed (1 minute pour rotation complete)
    # 60 = 1 seconde pour rotation complete
    def setVertSpeed(self, speed = 0):
        self.controller.setSpeed(self.VERT, speed)

    #methode permettant d'obtenir la position actuelle
    def getHorPos(self):
        position = self.controller.getPosition(self.HOR)
        return (position - 6000)/4

    #methode permettant d'obtenir la position actuelle
    def getVertPos(self):
        position = self.controller.getPosition(self.VERT)
        return (position - 2500)/3.5

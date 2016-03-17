import maestro

#classe permettant de controller le moteur du prehenseur
#le servomoteur doit etre branché sur le 3e port (milieu)
class PrehenseurRotationControl:
	
    def __init__(self, usb):
        self.MIN = 2500
        self.MAX = 7000
        self.CHANNEL = 3
        self.controller = maestro.Controller(usb)
        self.setVertSpeed()
        self.setHorSpeed()
        self.controller.setRange(self.CHANNEL, self.MIN, self.MAX)
        self.sleep()
    
    #position de repos
    def sleep(self):
    	self.controller.setTarget(self.CHANNEL, self.MIN)

    #methode permettant de definir la potition du servomoteur
    #units: position on unites, de 0 à 1000
    def setTarget(self, units):
        target = (units*4.5) + 2500
        self.controller.setTarget(self.CHANNEL, target)

    #methode permettant de définir une vitesse de transition
    # 0 = max speed
    # 1 = min speed (1 minute pour rotation complete)
    # 60 = 1 seconde pour rotation complete
    def setSpeed(self, speed = 0):
        self.controller.setSpeed(self.CHANNEL, speed)

    #methode permettant d'obtenir la position actuelle
    #de 0 à 1000
    def getPos(self):
        position = self.controller.getPosition(self.HOR)
        return (position - 2500)/4.5

    #methode permettant de mettre le prehenseur en position
    #de grab (à l'horizontal)
    def grab(self):
    	setTarget(0)

    #methode permettantde mettre le prehenseur en position
    #de lift (à la verticale) 
    def lift(self):
    	setTarget(1000)

from maestroControl import maestro

# classe permettant de controller le moteur du prehenseur
# le servomoteur doit etre branche sur le 3e port (milieu)
class PrehenseurRotationControl:

    def __init__(self, usb):
        #paramètres identifies
        self.__MIN = 4300
        self.__MAX = 8800
        self.__CHANNEL = 3
        self.__CONV_FACTOR = (self.__MAX - self.__MIN)/90
        self.__controller = maestro.Controller(usb)
        #init des parametres
        self.__controller.setRange(self.__CHANNEL, self.__MIN, self.__MAX)
        self.__setSpeed()
        self.sleep()

    # position de repos
    def sleep(self):
        self.__controller.setTarget(self.__CHANNEL, self.__MIN)

    #methode permettant de definir la potition du servomoteur
    #units: position on unites, de 0 a 90
    def setTarget(self, angle):
        target = int(angle*self.__CONV_FACTOR) + self.__MIN
        self.__controller.setTarget(self.__CHANNEL, target)

    #methode permettant de definir une vitesse de transition
    # 0 = max speed
    # 1 = min speed (1 minute pour rotation complete)
    # 60 = 1 seconde pour rotation complete
    def setSpeed(self, speed = 40):
        self.__controller.setSpeed(self.__CHANNEL, speed)

    #methode permettant d'obtenir la position actuelle
    #de 0 a 90
    def getPos(self):
        position = self.__controller.getPosition(self.__HOR)
        return (position - self.__MIN)/self.__CONV_FACTOR

    #methode permettant de mettre le prehenseur en position
    #de grab (a l'horizontal)
    def grab(self):
        self.__controller.setTarget(self.__CHANNEL, self.__MIN)

    #methode permettantde mettre le prehenseur en position
    #de lift (a la verticale) 
    def lift(self):
        self.__controller.setTarget(self.__CHANNEL, self.__MAX)

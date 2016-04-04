import maestro

#classe permettant de controller la camera sur deux axes de rotation.
#le servomoteur du haut (self.VERTical) doit etre branche sur le 
#5e port du pololu, le servomoteur du bas (self.HORizontal) doit etre
#branche sur le 4e port 
class CameraRotationControl:
	
    def __init__(self, usb):
    	#constantes identifiees des servomoteurs
        self.__MIDDLE = 6000
        self.__VERT_MAX = 6000
        self.__VERT_MIN = 2500
        self.__HOR_MAX = 10000
        self.__HOR_MIN = 2000
        self.__HOR_CONV_FACTOR = (self.__MIDDLE-self.__MIN)/90
        self.__VERT_CONV_FACTOR = (self.__MAX-self.__MIN)/90
        #channels des servomoteurs
        self.__HOR = 4
        self.__VERT = 5

        self.__controller = maestro.Controller(usb)
        self.setVertSpeed()
        self.setHorSpeed()
        self.controller.setRange(self.__HOR, self.__HOR_MIN, self.__HOR_MAX)
        self.controller.setRange(self.__VERT, self.__VERT_MIN, self.__VERT_MAX)
        self.sleep()
    
    #position de repos
    def sleep(self):
    	self.controller.setTarget(self.__HOR, self.__MIDDLE)
    	self.controller.setTarget(self.__VERT, self.__MIDDLE)

    #methode permettant de definir la potition horizontale de la camera
    #angle: position en degres, de -90 a 90
    def setHor(self, angle):
        target = int(angle*self.__HOR_CONV_FACTOR) + self.__MIDDLE
        self.__controller.setTarget(self.__HOR, target)

    #methode permettant de definir la potition horizontale de la camera
    #angle: position en units, de 0 a 90
    def setVert(self, angle):
        target = int(angle * self.__VERT_CONV_FACTOR) + self.__VERT_MIN
        self.__controller.setTarget(self.__VERT, target)

    #methode permettant de bouger la camera d'un nombre d'unites. 
    #de -180 a 180. limite automatiquement
    def moveHor(self, angle):
        currentPos = self.__controller.getPosition(self.__HOR)
        target = currentPos + int(angle * __HOR_CONV_FACTOR)
        self.__controller.setTarget(self.__HOR, target)


    #methode permettant de bouger la camera d'un nombre d'unites. 
    #de -90 a 90. limite automatiquement
    def moveVert(self, angle):
        currentPos = self.__controller.getPosition(self.__VERT)
        target = currentPos + int(angle * __VERT_CONV_FACTOR)
        self.__controller.setTarget(self.__VERT, target)

    #methode permettant de definir une vitesse de transition
    # 0 = max speed
    # 1 = min speed (1 minute pour rotation complete)
    # 60 = 1 seconde pour rotation complete
    def setHorSpeed(self, speed = 0):
        self.__controller.setSpeed(self.__HOR, speed)


    #methode permettant de definir une vitesse de transition
    # 0 = max speed
    # 1 = min speed (1 minute pour rotation complete)
    # 60 = 1 seconde pour rotation complete
    def setVertSpeed(self, speed = 0):
        self.__controller.setSpeed(self.__VERT, speed)

    #methode permettant d'obtenir la position actuelle
    def getHorPos(self):
        position = self.__controller.getPosition(self.__HOR)
        return (position - self.__MIDDLE)/self.__HOR_CONV_FACTOR

    #methode permettant d'obtenir la position actuelle
    def getVertPos(self):
        position = self.__controller.getPosition(self.__VERT)
        return (position - self.__VERT_MIN)/self.__VERT_CONV_FACTOR
        

class MagnetSimulation:
    def __init__(self):
        self.__activated = False
        self.__prehenseur_up = False

    def activate(self):
        self.__activated = True

    def deactivate(self):
        self.__activated = False

    def lift_up(self):
        self.__prehenseur_up = True

    def lift_down(self):
        self.__prehenseur_up = False

from threading import Thread
from time import sleep

class MagnetSimulation:
    def __init__(self):
        self.__activated = False
        self.__prehenseur_up = False
        self.__charge = 0

    def activate(self):
        self.__activated = True
        self.__charge -= 8 

    def deactivate(self):
        self.__activated = False

    def lift_up(self):
        self.__prehenseur_up = True

    def lift_down(self):
        self.__prehenseur_up = False

    def recharge(self, callback):
        self.thread = Thread(target=self.__thread_recharge, args=(callback,))
        self.thread.setDaemon(True)
        self.thread.start()

    def __thread_recharge(self, callback):
        while self.__charge < 90:
            self.__charge += 1
            sleep(0.05)
        callback()

    def discharge(self):
        while self.__charge > 5.0:
            self.__charge -= 1
            sleep(0.05)

    def get_charge(self):
        return self.__charge

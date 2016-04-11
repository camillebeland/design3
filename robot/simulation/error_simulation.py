import random
from robot.simulation.simulation_robot import SimulationWheels


class NoisyWheels(SimulationWheels):
    def __init__(self, worldmap, refresh_time, wheels_velocity, noise):
        super().__init__(worldmap, refresh_time = refresh_time, wheels_velocity=wheels_velocity)
        self.__noise = noise

    def move(self, x_pos, y_pos):
        noisy_x = x_pos + random.randint(-self.__noise,self.__noise)
        noisy_y = y_pos + random.randint(-self.__noise,self.__noise)
        super().move(noisy_x, noisy_y)

    def close_connection(self):
        pass

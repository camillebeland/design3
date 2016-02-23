from robot.simulation_robot import SimulationWheels
import random

class NoisyWheels(SimulationWheels):
    def move(self, x_pos, y_pos):
        noisy_x = x_pos + random.randint(-20,20)
        noisy_y = y_pos + random.randint(-20,20)
        super().move(noisy_x, noisy_y)

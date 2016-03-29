from robot.action import Action


class DiscoverManchesterCodeAction(Action):

    def __init__(self, robot, robot_service, worldmap, embedded_camera):
        super().__init__(robot, robot_service, worldmap, embedded_camera)

    def start(self):
        self._robot.find_manchester_code()

    def stop(self):
        raise NotImplementedError

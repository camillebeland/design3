class Action:
    def __init__(self, robot, robot_service, worldmap, embedded_camera):
        self._embedded_camera = embedded_camera
        self._robot = robot
        self._robot_service = robot_service
        self._worldmap = worldmap

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

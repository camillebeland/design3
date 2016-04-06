class Context:
    def __init__(self, robot, robot_service, worldmap, embedded_camera, event_listener):
        self.embedded_camera = embedded_camera
        self.robot = robot
        self.robot_service = robot_service
        self.worldmap = worldmap
        self.event_listener = event_listener

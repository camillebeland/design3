class Context:
    def __init__(self, robot, robot_service, worldmap, embedded_camera, event_listener, treasure_easiest_path, timer, vision_refresher):
        self.embedded_camera = embedded_camera
        self.robot = robot
        self.robot_service = robot_service
        self.worldmap = worldmap
        self.event_listener = event_listener
        self.treasure_easiest_path = treasure_easiest_path
        self.timer = timer
        self.vision_refresher = vision_refresher

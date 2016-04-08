class RobotInfo:
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle

    def to_dict(self):
        dict = {}
        dict['position'] = self.position.to_dict()
        dict['angle'] = self.angle
        return dict

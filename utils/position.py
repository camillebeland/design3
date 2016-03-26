class Position:

    def __init__(self, x_position, y_position):
        self.x = x_position
        self.y = y_position

    def to_dict(self):
        dict = {}
        dict['x'] = self.x
        dict['y'] = self.y
        return dict

    def to_tuple(self):
        return self.x, self.y

    def __eq__(self, other):
        if other.x == self.x and other.y == self.y:
            return True
        else:
            return False


    def __str__(self):
        return "Position: x:" + str(self.x) + ", y:" + str(self.y)

class Polygon:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def contains(self, cell):
        return (abs(self.x - cell.x) <= (cell.width + self.size)/2.0 and
                abs(self.y - cell.y) <= (cell.height + self.size)/2.0)

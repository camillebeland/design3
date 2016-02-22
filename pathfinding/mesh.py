from functools import reduce

class Cell:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def area(self):
        return self.width * self.height

    def split(self):
        return [
            Cell(self.width/2.0, self.height/2.0, self.x - self.width/4.0,self.y -self.height/4.0),
            Cell(self.width/2.0, self.height/2.0, self.x - self.width/4.0,self.y +self.height/4.0),
            Cell(self.width/2.0, self.height/2.0, self.x + self.width/4.0,self.y -self.height/4.0),
            Cell(self.width/2.0, self.height/2.0, self.x + self.width/4.0,self.y +self.height/4.0),
        ]

    def contains_any(self, obstacles):
        return reduce(lambda x,y : x or y,
                      map(self.contains, obstacles),
                      False
        )

    def __str__(self):
        return "({0},{1},{2},{3})".format(self.x, self.y, self.width, self.height)

    def contains(self, obstacle):
        return obstacle.distance(self) < (self.width/2.0 + self.height/2.0 + obstacle.size)**2

    def contains_point(self, point):
        x, y = point
        return (x >= (self.x - self.width/2.0) and
                x <= (self.x + self.width/2.0) and
                y >= (self.y - self.height/2.0) and
                y <= (self.y + self.height/2.0))

    def is_adjacent_to(self, other_cell):
        return (((abs(self.x - other_cell.x) - (self.width + other_cell.width)/2.0) < 1e-6 and
                abs(self.y - other_cell.y) < (self.height + other_cell.height)/2.0) or
                ((abs(self.y - other_cell.y) - (self.height + other_cell.height)/2.0) < 1e-6 and
                abs(self.x - other_cell.x) < (self.width + other_cell.width)/2.0))

    def partitionCells(self, obstacles, area_treshold):
        if(self.area() < area_treshold):
            return []
        elif(self.contains_any(obstacles)):
            childCells = self.split()
            return reduce(lambda x, y: x+y,
                          map(lambda cell: cell.partitionCells(obstacles, area_treshold), childCells))
        else:
            return [self]

class Mesh:
    def __init__(self, cells):
        self.__cells = cells

    def get_cells(self):
        return self.__cells

class polygon:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def distance(self, target):
        return (self.x - target.x)**2 + (self.y - target.y)**2


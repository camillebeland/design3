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
        return reduce(lambda x, y: x or y,
                      map(self.contains, obstacles),
                      False
        )

    def __str__(self):
        return "({0},{1},{2},{3})".format(self.x, self.y, self.width, self.height)

    def contains(self, obstacle):
        return obstacle.contains(self)

    def contains_point(self, point):
        x = point.x
        y = point.y
        return ((self.x - self.width / 2.0) <= x <= (self.x + self.width / 2.0) and
                (self.y - self.height / 2.0) <= y <= (self.y + self.height / 2.0))

    def is_adjacent_to(self, other_cell):
        return (((abs(self.x - other_cell.x) - (self.width + other_cell.width)/2.0) < 1e-6 and
                abs(self.y - other_cell.y) < (self.height + other_cell.height)/2.0) or
                ((abs(self.y - other_cell.y) - (self.height + other_cell.height)/2.0) < 1e-6 and
                abs(self.x - other_cell.x) < (self.width + other_cell.width)/2.0))

    def partition_cells(self, obstacles, area_treshold):
        if(self.area() < area_treshold):
            return []
        elif(self.contains_any(obstacles)):
            childCells = self.split()
            return reduce(lambda x, y: x+y,
                          map(lambda cell: cell.partition_cells(obstacles, area_treshold), childCells))
        else:
            return [self]




def importworking ():
    print("Ca marche")

class Robot:
    def __init__ (self):
        self.x = 0
        self.y = 0
        self.width = 1
        self.height = 1

    def print (self):
        print('({0} , {1})'.format(self.x, self.y))

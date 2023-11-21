#Basic xy coordinate definition
class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    #comparison function override for searching
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

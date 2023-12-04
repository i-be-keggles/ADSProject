import random

#all O(1)
#Basic xy coordinate definition
class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    #comparison function override for searching
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    #addition function overrides for simpler syntax
    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return Coords(other.x + self.x, other.y + self.y)


#O(1)
#generates random offset with length clamps
def randomMinMaxRange(min, max):
    #randomize quadrant
    nx = ny = 1
    if random.randint(0,100) <= 50:
        nx *= -1
    if random.randint(0,100) <= 50:
        ny *= -1

    #calculate pos
    return Coords(random.randint(min, max + 1) * nx, random.randint(min, max + 1) * ny)


#best: O(1), worst: O(n^2) where n is 2*radius
#calculate if there is a mine within r spaces of position
def mineInRange(x, y, r, board):
    size = len(board)
    for dx in range(max(0, x-r), min(size, x+r+1)):
        for dy in range(max(0, y-r), min(size, y+r+1)):
            if board[dy][dx] == "mine":
                return True
    return False


#O(1)
#check if there is a mine on given tile
def mineAtLocation(x, y, mines):
    for mine in mines:
        if mine.x == x and mine.y == y:
            return True
    return False


#O(1)
#calculate the numbers of mines within 1 tile of position
def minesNextTo(x, y, mines, size):
    n = 0
    for dx in range(max(0, x-1), min(size, x+2)):
        for dy in range(max(0, y-1), min(size, y+2)):
            if mineAtLocation(dx, dy, mines):
                n += 1
    return n
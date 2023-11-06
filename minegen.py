from util import Coords
import random

def generateMinesPoisson(board, numMines):
    mines = []
    #TODO: generate coords with poisson disc sampling
    return mines


#old solution
def generateMines(board, numMines, size, mineAtLocation):
    mines = []
    for i in range(numMines):
        x = y = -1
        while(x == -1 or mineAtLocation(x,y)):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
        mines.append(Coords(x,y))
        board[y][x] == "mine"
    return mines
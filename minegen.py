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
        #check for overlap
        while(x == -1 or mineAtLocation(x,y)):
            #generate random position
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
        #save and add to board
        mines.append(Coords(x,y))
        board[y][x] == "mine"
    return mines
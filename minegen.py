from util import *

#O(n) where n is the number of generated mines
#https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf
#generate mine positions with poisson disc sampling algorithm - bfs based
def generateMinesPoisson(board, spacing, attempts = 20):
    mines = []
    size = len(board)

    #initialize sample
    points = [Coords(random.randint(0, size - 1), random.randint(0, size - 1))]
    board[points[-1].y][points[-1].x] = "mine"
    
    while len(points) > 0:
        #pick random point
        p = points[random.randint(0,len(points)-1)]
        for i in range(attempts):
            #generate point between r and 2r units from the active point
            c = p + randomMinMaxRange(spacing, 2*spacing)
            #check for overlap
            if 0 <= c.x < size and 0 <= c.y < size and not mineInRange(c.x, c.y, spacing, board):
                points.append(c)
                mines.append(c)
                board[c.y][c.x] = "mine"
        #remove if no points
        if points[-1] == p:
            points.remove(p)

    return mines


#O(n) where n is the number of mines
#generate mines randomly
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
from game2dboard import Board
import minegen as mg
from util import *

size = 10
cellSize = 25

numMines = 7
mineSpacing = 2

flags = []
mines = []
b = None


#O(1) but may call functions with higher time complexity (eg. checkWin: up to O(n*m+p))
#user interaction logic
def handleClick(btn, row, col):
	#check for blank space
	if b[row][col] != "cover" and b[row][col] != "flag":
		return
	#try clearing
	if btn == 1 and b[row][col] != "flag":
		if mineAtLocation(col, row, mines):
			b[row][col] = "mine"
			print("You lose!")
			
		else:
			clearTiles(col, row);
	#flag placement
	elif btn == 3:
		#remove flag
		if b[row][col] == "flag":
			b[row][col] = "cover"
			flags.remove(Coords(row,col))
		#place flag
		else:
			if(len(flags) == len(mines)):
				print("No more flags.")
				return
			b[row][col] = "flag"
			flags.append(Coords(row,col))
	#check for win
	if checkWin():
		print("You win!")


#O(n*m) where n,m are dimensions
#debug function - displays neighbouring mines for each tile
def generateNumbers():
	for y in range(0, size):
		for x in range(0, size):
			if not mineAtLocation(x,y, mines) and minesNextTo(x,y, mines) != 0:
				b[y][x] = minesNextTo(x,y, mines, size)


#best:O(1), worst:O(n*m+p) where n,m are dimensions, p is flags
#checks for win condition (all mines must be flagged with no other covered spaces)
def checkWin():
	print(len(flags),"out of", len(mines), "flags.")
	#check if all flags have been placed
	if len(mines) != len(flags):
		return False
	#check if all tiles have been cleared
	for y in range(0, size):
		for x in range(0, size):
			if b[y][x] == "cover":
				print("Clear all tiles to win.")
				return False
	#check that flags are correct
	for flag in flags:
		if not mineAtLocation(flag.y, flag.x, mines):
			return False
	return True


#best:O(1), worst:O(n*m) where n,m are dimensions
#depth first search floodfill
def clearTiles(x,y):
	#base case
	if x < 0 or y < 0 or x >= size or y >= size or b[y][x] == None:
		return

	#calculate and display neighbouring mines
	m = minesNextTo(x,y, mines, size)
	if m != 0:
		b[y][x] = m
		return

	#clear if 0
	b[y][x] = None

	#recurse
	clearTiles(x + 1, y)
	clearTiles(x - 1, y)
	clearTiles(x, y + 1)
	clearTiles(x, y - 1)


#initialise game
b = Board(size, size)

b.title = "MineSweeper"
b.cell_size = cellSize       
b.cell_color = "white"

#mines = mg.generateMines(b, numMines, size, mineAtLocation)
mines = mg.generateMinesPoisson(b, mineSpacing)
#generateNumbers()

b.fill("cover")

b.on_mouse_click = handleClick
b.show()
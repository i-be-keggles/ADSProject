from game2dboard import Board
import random
import minegen as mg
from util import Coords

size = 10
cellSize = 25

numMines = 7

flags = []
mines = []
b = None


#user interaction logic
def handleClick(btn, row, col):
	#check for blank space
	if b[row][col] != "cover" and b[row][col] != "flag":
		return
	#try clearing
	if btn == 1 and b[row][col] != "flag":
		if mineAtLocation(col, row):
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


#check if there is a mine on given tile
def mineAtLocation(x, y):
	for mine in mines:
		if mine.x == x and mine.y == y:
			return True
	return False


#calculate the numbers of mines within 1 tile of position
def minesInRange(x, y):
	n = 0
	for dx in range(max(0, x-1), min(size, x+2)):
		for dy in range(max(0, y-1), min(size, y+2)):
			if mineAtLocation(dx, dy):
				n += 1
	return n


#debug function - displays neighbouring mines for each tile
def generateNumbers():
	for y in range(0, size):
		for x in range(0, size):
			if not mineAtLocation(x,y) and minesInRange(x,y) != 0:
				b[y][x] = minesInRange(x,y)


#checks for win condition (all mines must be flagged with no other covered spaces)
def checkWin():
	print(len(flags),"out of", len(mines), "flags.")
	#check if all flags have been placed
	if len(mines) != len(flags):
		return False
<<<<<<< HEAD
	#check if all tiles have been cleared
=======
>>>>>>> 1fead01 (flag logic update & win condition tweak)
	for y in range(0, size):
		for x in range(0, size):
			if b[y][x] == "cover":
				print("Clear all tiles to win.")
				return False
	#check that flags are correct
	for flag in flags:
		if not mineAtLocation(flag.y, flag.x):
			return False
	return True

#depth first search floodfill
def clearTiles(x,y):
	if x < 0 or y < 0 or x >= size or y >= size or b[y][x] == None:
		return
	m = minesInRange(x,y)
	if m != 0:
		b[y][x] = m
		return

#depth first search floodfill
def clearTiles(x,y):
	#base case
	if x < 0 or y < 0 or x >= size or y >= size or b[y][x] == None:
		return

	#calculate and display neighbouring mines
	m = minesInRange(x,y)
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

b.fill("cover")

mines = mg.generateMines(b, numMines, size, mineAtLocation)
#mines = mg.generateMinesPoisson(b, numMines)
#generateNumbers()

b.on_mouse_click = handleClick
b.show()
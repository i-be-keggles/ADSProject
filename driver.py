from game2dboard import Board
import random
import minegen as mg
from util import Coords

size = 10
cellSize = 25

numMines = 20

flags = []
mines = []
b = None



def handleClick(btn, row, col):
	if b[row][col] != "cover" and b[row][col] != "flag":
		return
	if btn == 1 and b[row][col] != "flag":
		if mineAtLocation(col, row):
			b[row][col] = "mine"
			print("You lose!")
		else:
			clearTiles(col, row);
	elif btn == 3:
		if b[row][col] == "flag":
			b[row][col] = "cover"
			flags.remove(coords(row,col))
		else:
			b[row][col] = "flag"
			flags.append(coords(row,col))
		if checkWin():
			print("You win!")


def mineAtLocation(x, y):
	for mine in mines:
		if mine.x == x and mine.y == y:
			return True
	return False


def minesInRange(x, y):
	n = 0
	for dx in range(max(0, x-1), min(size, x+2)):
		for dy in range(max(0, y-1), min(size, y+2)):
			if mineAtLocation(dx, dy):
				n += 1
	return n


def generateNumbers():
	for y in range(0, size):
		for x in range(0, size):
			if not mineAtLocation(x,y):
				b[y][x] = minesInRange(x,y)


def checkWin():
	if len(mines) != len(flags):
		return False
	for flag in flags:
		if not mineAtLocation(x,y):
			return False
	return True


def clearTiles(x, y):
	b[y][x] = None
	print("Function not implemented.")
	pass


b = Board(size, size)

b.title = "MineSweeper"
b.cell_size = cellSize       
b.cell_color = "white"

b.fill("cover")

#mines = mg.generateMines(b, numMines, size, mineAtLocation)
mines = mg.generateMinesPoisson(b, numMines)
generateNumbers()

b.on_mouse_click = handleClick
b.show()
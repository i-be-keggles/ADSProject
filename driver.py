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
			flags.remove(Coords(row,col))
		else:
			b[row][col] = "flag"
			flags.append(Coords(row,col))
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
			if not mineAtLocation(x,y) and minesInRange(x,y) != 0:
				b[y][x] = minesInRange(x,y)


def checkWin():
	if len(mines) != len(flags):
		print(len(flags),"out of", len(mines), "flags.")
		return False
	for flag in flags:
		if not mineAtLocation(flag.y, flag.x):
			print("Misplaced flag at", flag.x, flag.y)
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

	b[y][x] = None
	clearTiles(x + 1, y)
	clearTiles(x - 1, y)
	clearTiles(x, y + 1)
	clearTiles(x, y - 1)

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
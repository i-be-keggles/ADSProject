from game2dboard import Board

from data_structures import BoardGraph
from algorithms import *
from scoreboard import *

import minegen as mg
from util import *
import time

size = 10
cellSize = 25

numMines = 7
mineSpacing = 2

flags = []
mines = []
b = None

scoreboard_path = "scoreboard.txt"


#	user interaction logic
def handleClick(btn, row, col):
	#check for blank space
	if b[row][col] != "cover" and b[row][col] != "flag":
		return
	#try clearing
	if btn == 1 and b[row][col] != "flag":
		if mineAtLocation(col, row, mines):
			b[row][col] = "mine"
			print("You lose!")
			return -1
		else:
			clearTiles(col, row)
	#flag placement
	elif btn == 3:
		#remove flag
		if b[row][col] == "flag":
			b[row][col] = "cover"
			flags.remove(Coords(row, col))
		#place flag
		else:
			if(len(flags) == len(mines)):
				print("No more flags.")
				return
			b[row][col] = "flag"
			flags.append(Coords(row, col))
	#check for win
	if checkWin():
		print("You win!")
		return 0


#debug function - displays neighbouring mines for each tile
def generateNumbers():
	for y in range(0, size):
		for x in range(0, size):
			if not mineAtLocation(x,y, mines) and minesNextTo(x,y, mines) != 0:
				b[y][x] = minesNextTo(x,y, mines, size)


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


#depth first search floodfill
def clearTiles(x, y):
	node = b.get_node(x, y)
	# Base case
	if node is None or node.value == None:
		return

	# Calculate and display neighbouring mines
	m = minesNextTo(x, y, mines, size)
	if m != 0:
		node.value = m
		return

	# Clear if 0
	node.value = None

	# Recurse through adjacent nodes
	for adj_node in node.adjacent:
		clearTiles(adj_node.x, adj_node.y)


def main():
	global b, flags, mines
	#initialise game
	b = BoardGraph(size)
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


if __name__ == '__main__':
	start = time.time()
	main()
	clear_time = time.time() - start
	update_scoreboard(scoreboard_path, clear_time, "HARD")

from game2dboard import Board
from datastructures import Graph
from algorithms import quicksort, minesNextTo

import random
import time


"""
The time complexities are written at function definitions, not function calls.
"""

# Constants
SIZE = 10
NUM_MINES = 15
SCOREBOARD_PATH = "scoreboard.txt"

# Globals
logical_board = Graph(SIZE)
visual_board = Board(SIZE, SIZE)
start_time = time.time()
mines = []


<<<<<<< HEAD
def place_mines():  # Average: O(n), Worst: O(n^2)
    global mines
    mines.clear()

    while len(mines) < NUM_MINES:
        x, y = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
        if (x, y) not in mines:
            mines.append((x, y))
            logical_board.get_node(x, y).value = 'mine'


def handleClick(btn, row, col):     # Average: O(1), Worst: O(1)
    node = logical_board.get_node(row, col)

    if btn == 3:
        if visual_board[row][col] == 'cover':
            visual_board[row][col] = 'flag'
            node.value = 'flag'
        elif visual_board[row][col] == 'flag':
            visual_board[row][col] = 'cover'
            node.value = 'cover'
        return

    if btn == 1:
        if node.value == 'cover':
            clearTiles(row, col)
            check_win_condition()
        elif node.value == 'mine':
            reveal_mines()
            print("Game Over! You hit a mine.")


def reveal_mines():     # Average: O(n), Worst: O(n) where n is the number of cells
    for x in range(SIZE):
        for y in range(SIZE):
            if logical_board.get_node(x, y).value == 'mine':
                visual_board[x][y] = 'mine'


def clearTiles(x, y, visited=None):     # Average: O(n), Worst: O(n)
    if visited is None:
        visited = set()
=======
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
>>>>>>> main

    if x < 0 or y < 0 or x >= SIZE or y >= SIZE:
        return
    if (x, y) in visited:
        return
    if logical_board.get_node(x, y).value != 'cover':
        return

    visited.add((x, y))

    adjacent_mines = minesNextTo(x, y, mines, SIZE)
    logical_board.get_node(x, y).value = str(adjacent_mines) if adjacent_mines > 0 else 'clear'
    visual_board[x][y] = str(adjacent_mines) if adjacent_mines > 0 else None  # Use 'None' to clear the cell

<<<<<<< HEAD
    if adjacent_mines == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                clearTiles(x + dx, y + dy, visited)
=======

#initialise game
b = Board(size, size)
>>>>>>> main


def count_adjacent_mines(x, y):     # Average: O(1), Worst: O(1)
    count = 0
    for node in logical_board.get_node(x, y).adjacent:
        if node.value == 'mine':
            count += 1
    return count


def check_win_condition():      # Average: O(n), Worst: O(n)
    if all(node.value != 'cover' for row in logical_board.nodes for node in row if node.value != 'mine'):
        print("Congratulations! You've cleared all mines.")
        update_scoreboard(SCOREBOARD_PATH, time.time() - start_time)


def update_scoreboard(file_path, new_score):    # Average: O(n log n), Worst: O(n^2)
    try:
        with open(file_path, 'r') as file:
            scores = [float(line.split(') ')[1]) for line in file if line.strip()]
    except FileNotFoundError:
        scores = []

    scores.append(round(float(new_score), 3))
    ranked_scores = quicksort(scores)

    with open(file_path, 'w') as file:
        for i, score in enumerate(ranked_scores, start=1):
            file.write(f"{i}) {score}\n")

    print(f"Score saved to {SCOREBOARD_PATH}")


def main():     # Average: O(n), Worst: O(n) dominated by the reveal_mines or clearTiles
    place_mines()

    visual_board.cell_size = 25
    visual_board.on_mouse_click = handleClick
    visual_board.fill('cover')
    visual_board.show()


if __name__ == '__main__':
    main()

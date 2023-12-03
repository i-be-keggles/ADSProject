from game2dboard import Board
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


def get_scoreboard(path):
	try:
		with open(path, "r") as f:
			return f.readlines()
	except FileNotFoundError:
		return ""


def update_scoreboard(scoreboard_file, time, difficulty):
	try:
		with open(scoreboard_file, 'r') as f:
			content = f.read()
	except FileNotFoundError:
		content = "===EASY===\n\n===MEDIUM===\n\n===HARD===\n"

	sections = {"EASY": [], "MEDIUM": [], "HARD": []}
	current_section = None

	for line in content.split('\n'):
		if line.startswith("==="):
			current_section = line.strip("= \n")
		elif line and current_section:
			sections[current_section].append(line.split(') ')[1])

	sections[difficulty].append(format_time(time))
	sorted_times = quicksort(sections[difficulty])

	new_content = ""
	for diff in ["EASY", "MEDIUM", "HARD"]:
		new_content += f"==={diff}===\n" + format_section(sorted_times if diff == difficulty else sections[diff]) + "\n"

	with open(scoreboard_file, 'w') as f:
		f.write(new_content.strip())


def format_time(time):
	minutes, seconds = divmod(time, 60)
	seconds, milliseconds = divmod(seconds, 1)
	return f"{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds * 100):02d}"


def format_section(times):
	return '\n'.join(f"{i + 1}) {time}" for i, time in enumerate(times))


def quicksort(times):
	if len(times) <= 1:
		return times
	pivot = times[len(times) // 2]
	left = [x for x in times if x < pivot]
	middle = [x for x in times if x == pivot]
	right = [x for x in times if x > pivot]
	return quicksort(left) + middle + quicksort(right)


def main():
	global b, flags, mines
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


if __name__ == '__main__':
	start = time.time()
	main()
	clear_time = time.time() - start
	update_scoreboard(scoreboard_path, clear_time, "HARD")

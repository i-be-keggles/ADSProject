from game2dboard import Board
import minegen as mg
from util import *
import time
import tkinter as tk

size = 10
cellSize = 25
numMines = 7
mineSpacing = 2
flags = []
mines = []
b = None
game_active = False
scoreboard_path = "scoreboard.txt"

def startMenu():
    def onDifficultySelect(difficulty):
        global size, numMines, mineSpacing
        if difficulty == "EASY":
            size, numMines, mineSpacing = 10, 7, 2
        elif difficulty == "MEDIUM":
            size, numMines, mineSpacing = 15, 20, 2
        elif difficulty == "HARD":
            size, numMines, mineSpacing = 20, 40, 2
        root.destroy()
        main()
    root = tk.Tk()
    root.title("Select Difficulty")
    tk.Button(root, text="EASY", command=lambda: onDifficultySelect("EASY")).pack()
    tk.Button(root, text="MEDIUM", command=lambda: onDifficultySelect("MEDIUM")).pack()
    tk.Button(root, text="HARD", command=lambda: onDifficultySelect("HARD")).pack()
    root.mainloop()

def loseScreen():
    def retry():
        root.destroy()
        startMenu()
    root = tk.Tk()
    root.title("Game Over")
    tk.Label(root, text="You lose!").pack()
    tk.Button(root, text="Retry", command=retry).pack()
    root.mainloop()

def winScreen(clear_time):
    def saveScore():
        update_scoreboard(scoreboard_path, clear_time, get_difficulty())
        print("Score saved!")
    def playAgain():
        root.destroy()
        startMenu()
    root = tk.Tk()
    root.title("Congratulations!")
    tk.Label(root, text="You win!").pack()
    tk.Button(root, text="SAVE SCORE", command=saveScore).pack()
    tk.Button(root, text="PLAY AGAIN", command=playAgain).pack()
    root.mainloop()

def get_difficulty():
    if size == 10:
        return "EASY"
    elif size == 15:
        return "MEDIUM"
    else:
        return "HARD"

def handleClick(btn, row, col):
    global b, flags, mines, game_active
    if not game_active:
        return
    if b[row][col] != "cover" and b[row][col] != "flag":
        return
    if btn == 1 and b[row][col] != "flag":
        if mineAtLocation(col, row, mines):
            b[row][col] = "mine"
            print("You lose!")
            game_active = False
            loseScreen()
            return
        else:
            clearTiles(col, row)
    elif btn == 3:
        if b[row][col] == "flag":
            b[row][col] = "cover"
            flags.remove(Coords(row, col))
        else:
            if(len(flags) == len(mines)):
                print("No more flags.")
                return
            b[row][col] = "flag"
            flags.append(Coords(row, col))
    if checkWin():
        print("You win!")
        game_active = False
        clear_time = time.time() - start
        winScreen(clear_time)

def generateNumbers():
    for y in range(0, size):
        for x in range(0, size):
            if not mineAtLocation(x,y, mines) and minesNextTo(x,y, mines) != 0:
                b[y][x] = minesNextTo(x,y, mines, size)

def checkWin():
    print(len(flags), "out of", len(mines), "flags.")
    if len(mines) != len(flags):
        return False
    for y in range(0, size):
        for x in range(0, size):
            if b[y][x] == "cover":
                print("Clear all tiles to win.")
                return False
    for flag in flags:
        if not mineAtLocation(flag.y, flag.x, mines):
            return False
    return True

def clearTiles(x, y):
    if x < 0 or y < 0 or x >= size or y >= size or b[y][x] == None:
        return
    m = minesNextTo(x, y, mines, size)
    if m != 0:
        b[y][x] = m
        return
    b[y][x] = None
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
    global b, flags, mines, start, game_active
    start = time.time()
    b = Board(size, size)
    b.title = "MineSweeper"
    b.cell_size = cellSize
    b.cell_color = "white"
    mines = mg.generateMinesPoisson(b, mineSpacing)
    b.fill("cover")
    b.on_mouse_click = handleClick
    game_active = True
    b.show()

if __name__ == '__main__':
    startMenu()

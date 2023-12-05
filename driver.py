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


# Function to place mines randomly on the board
def place_mines():  # Average: O(n), Worst: O(n^2)
    global mines
    mines.clear()

    # Randomly select and place mines, ensuring no duplicates
    while len(mines) < NUM_MINES:
        x, y = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
        if (x, y) not in mines:
            mines.append((x, y))    # front end implementation
            logical_board.get_node(x, y).value = 'mine'     # back end implementation


# Handles mouse click events on the board
def handleClick(btn, row, col):     # Average: O(1), Worst: O(1)
    node = logical_board.get_node(row, col)

    if btn == 3:    # Right click: flag
        if visual_board[row][col] == 'cover':
            visual_board[row][col] = 'flag'
            node.value = 'flag'
        elif visual_board[row][col] == 'flag':
            visual_board[row][col] = 'cover'
            node.value = 'cover'
        return

    if btn == 1:     # Left click: uncover
        if node.value == 'cover':
            clearTiles(row, col)
            check_win_condition()
        elif node.value == 'mine':
            reveal_mines()
            print("Game Over! You hit a mine.")
            visual_board.close()


# Recursively clears tiles without adjacent mines: FloodFill
def clearTiles(x, y, visited=None):     # Average: O(n), Worst: O(n)
    if visited is None:
        visited = set()

    # Base case checks for recursion
    if x < 0 or y < 0 or x >= SIZE or y >= SIZE:
        return
    if (x, y) in visited:
        return
    if logical_board.get_node(x, y).value != 'cover':
        return

    visited.add((x, y))     # Add to visited to prevent cycling

    # Update cell based on adjacent mines
    adjacent_mines = minesNextTo(x, y, mines, SIZE)
    logical_board.get_node(x, y).value = str(adjacent_mines) if adjacent_mines > 0 else 'clear'
    visual_board[x][y] = str(adjacent_mines) if adjacent_mines > 0 else None

    # Recurse for adjacent cells if no adjacent mines
    if adjacent_mines == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                clearTiles(x + dx, y + dy, visited)


# Reveals all mines on the board
def reveal_mines():     # Average: O(n), Worst: O(n) where n is the number of cells
    for x in range(SIZE):
        for y in range(SIZE):
            if logical_board.get_node(x, y).value == 'mine':
                visual_board[x][y] = 'mine'


# Counts the number of mines next to a specific tile
def count_adjacent_mines(x, y):     # Average: O(1), Worst: O(1)
    count = 0
    for node in logical_board.get_node(x, y).adjacent:
        if node.value == 'mine':
            count += 1
    return count


# Check if the win condition is met
def check_win_condition():      # Average: O(n), Worst: O(n)
    if all(node.value != 'cover' for row in logical_board.nodes for node in row if node.value != 'mine'):
        print("Congratulations! You've cleared all mines.")
        visual_board.close()
        update_scoreboard(SCOREBOARD_PATH, time.time() - start_time)    # Updates the scoreboard


# Updates the scoreboard with new scores
def update_scoreboard(file_path, new_score):    # Average: O(n log n), Worst: O(n^2)
    try:
        with open(file_path, 'r') as file:
            scores = [float(line.split(') ')[1]) for line in file if line.strip()]      # Get scores
    except FileNotFoundError:
        scores = []     # New scores list

    scores.append(round(float(new_score), 3))
    ranked_scores = quicksort(scores)       # Sort current scores

    with open(file_path, 'w') as file:
        for i, score in enumerate(ranked_scores, start=1):
            file.write(f"{i}) {score}\n")

    print(f"Score saved to {SCOREBOARD_PATH}")


# Main function to initialize and start the game
def main():     # Average: O(n), Worst: O(n) dominated by the reveal_mines or clearTiles
    place_mines()

    visual_board.cell_size = 25
    visual_board.on_mouse_click = handleClick
    visual_board.fill('cover')
    visual_board.show()


if __name__ == '__main__':
    main()

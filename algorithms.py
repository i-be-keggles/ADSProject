
# Quicksort function to rank scores
def quicksort(arr):     # Average: O(n log n), Worst: O(n^2)
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


# Calculate the numbers of mines within 1 tile of position
def minesNextTo(x, y, mines, size):     # Average: O(1), Worst: O(1)
    n = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and (nx, ny) in mines:
                n += 1
    return n

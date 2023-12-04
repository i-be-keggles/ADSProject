class Node:
    def __init__(self, x, y, value='cover'):
        self.x = x
        self.y = y
        self.value = value
        self.adjacent = []  # List of adjacent nodes

    def add_adjacent(self, node):
        self.adjacent.append(node)


class BoardGraph:
    def __init__(self, size):
        self.size = size
        self.nodes = [[Node(x, y) for y in range(size)] for x in range(size)]

        # Creating connections between adjacent nodes
        for x in range(size):
            for y in range(size):
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= x + dx < size and 0 <= y + dy < size and (dx != 0 or dy != 0):
                            self.nodes[x][y].add_adjacent(self.nodes[x + dx][y + dy])

    def get_node(self, x, y):
        return self.nodes[x][y]

    def update_value(self, x, y, value):
        self.nodes[x][y].value = value


class Node:
    def __init__(self, x, y, value='cover'):    # Average: O(1), Worst: O(1)
        self.x = x
        self.y = y
        self.value = value
        self.adjacent = []

    def add_adjacent(self, node):   # Average: O(1), Worst: O(1)
        self.adjacent.append(node)


class Graph:
    def __init__(self, size):    # Average: O(n^2), Worst: O(n^2)
        self.size = size
        self.nodes = [[Node(x, y) for y in range(size)] for x in range(size)]

        for x in range(size):
            for y in range(size):
                node = self.nodes[x][y]
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < size and 0 <= ny < size:
                            adj_node = self.nodes[nx][ny]
                            if adj_node not in node.adjacent:
                                node.adjacent.append(adj_node)

    def get_node(self, x, y):   # Average: O(1), Worst: O(1)
        return self.nodes[x][y]

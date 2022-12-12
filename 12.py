class Node:
    def __init__(self, token, row, col):
        self.token = token
        self.row = row
        self.col = col
        if token == 'S':
            self.height = 0
        elif token == 'E':
            self.height = ord('z')-ord('a')
        else:
            self.height = ord(token)-ord('a')
        self.edges = {'R':None, 'L':None, 'U':None, 'D':None}
        self.y = 2**15
        if token == 'S':
            self.y = 0

    def __lt__(self, other):
         return self.y < other.y

    def __repr__(self):
        return str(self.y)

def calc_min_distance_between_nodes(nodes, source, destination):
    # Run Dijkstra's algorithm
    unchecked_nodes = [node for node in nodes]
    for node in unchecked_nodes:
        node.y = 2**15
    source.y = 0
    current_node = source
    while len(unchecked_nodes) > 0:
        unchecked_nodes.sort()
        current_node = unchecked_nodes[0]
        unchecked_nodes.remove(current_node)
        for edge in current_node.edges:
            if current_node.edges[edge] is not None:
                if current_node.y + 1 < current_node.edges[edge].y:
                    current_node.edges[edge].y = current_node.y + 1
    return destination.y


with open('12i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]

# Create node graph
node_array = []
for r in range(len(lines)):
    node_array.append([])
    for c in range(len(lines[0])):
        node_array[r].append(Node(lines[r][c], r, c))
        if node_array[r][c].token == 'E':
            source_node = node_array[r][c]
        if node_array[r][c].token == 'S':
            exit_node = node_array[r][c]

# Create edges
all_nodes = []
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if 0 != r:
            if node_array[r-1][c].height >= node_array[r][c].height-1:
                node_array[r][c].edges['U'] = node_array[r-1][c]
        if len(lines)-1 != r:
            if node_array[r+1][c].height >= node_array[r][c].height-1:
                node_array[r][c].edges['D'] = node_array[r+1][c]
        if 0 != c:
            if node_array[r][c-1].height >= node_array[r][c].height-1:
                node_array[r][c].edges['L'] = node_array[r][c-1]
        if len(node_array[0])-1 != c:
            if node_array[r][c+1].height >= node_array[r][c].height-1:
                node_array[r][c].edges['R'] = node_array[r][c+1]
        all_nodes.append(node_array[r][c])

part_1 = calc_min_distance_between_nodes(all_nodes, source_node, exit_node)
print('Part 1: {:}'.format(part_1))
nodes_with_height_0 = [n for n in all_nodes if n.height == 0]
nodes_with_height_0.sort()
print('Part 2: {:}'.format(nodes_with_height_0[0]))

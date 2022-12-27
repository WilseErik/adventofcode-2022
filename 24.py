from matplotlib import pyplot as plt
import numpy as np
import matplotlib.image
from matplotlib.animation import FuncAnimation
import os.path
import heapq

UPWARDS_BLIZZARD  = 1 << 0      # 1
DOWNWARDS_BLIZZARD = 1 << 1     # 2
LEFT_BLIZZARD = 1 << 2          # 4
RIGHT_BLIZZARD = 1 << 3         # 8
WALL = 1 << 4                   # 16
UPDATE_SHIFT = 8

def print_map(valley_map):
    plt.imshow(valley_map, cmap='gnuplot2_r',interpolation='nearest')#,aspect='auto')
    plt.show()

def create_valley_map(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    valley = np.zeros((len(lines), len(lines[0])), dtype=np.uint16)
    for y in range(valley.shape[0]):
        for x in range(valley.shape[1]):
            if lines[y][x] == '#':
                valley[y,x] = WALL
            elif lines[y][x] == '^':
                valley[y,x] = UPWARDS_BLIZZARD
            elif lines[y][x] == 'v':
                valley[y,x] = DOWNWARDS_BLIZZARD
            elif lines[y][x] == '<':
                valley[y,x] = LEFT_BLIZZARD
            elif lines[y][x] == '>':
                valley[y,x] = RIGHT_BLIZZARD
    return valley

def advance_blizzards(valley):
    for y in range(valley.shape[0]):
        for x in range(valley.shape[1]):
            if valley[y,x] & UPWARDS_BLIZZARD != 0:
                if valley[y-1,x] & WALL != 0:
                    valley[valley.shape[0]-2,x] |= (UPWARDS_BLIZZARD << UPDATE_SHIFT)
                else:
                    valley[y-1,x] |= (UPWARDS_BLIZZARD << UPDATE_SHIFT)
            if valley[y,x] & DOWNWARDS_BLIZZARD != 0:
                if valley[y+1,x] & WALL != 0:
                    valley[1,x] |= (DOWNWARDS_BLIZZARD << UPDATE_SHIFT)
                else:
                    valley[y+1,x] |= (DOWNWARDS_BLIZZARD << UPDATE_SHIFT)
            if valley[y,x] & LEFT_BLIZZARD != 0:
                if valley[y,x-1] & WALL != 0:
                    valley[y,valley.shape[1]-2] |= (LEFT_BLIZZARD << UPDATE_SHIFT)
                else:
                    valley[y,x-1] |= (LEFT_BLIZZARD << UPDATE_SHIFT)
            if valley[y,x] & RIGHT_BLIZZARD != 0:
                if valley[y,x+1] & WALL != 0:
                    valley[y,1] |= (RIGHT_BLIZZARD << UPDATE_SHIFT)
                else:
                    valley[y,x+1] |= (RIGHT_BLIZZARD << UPDATE_SHIFT)
            if valley[y,x] & WALL != 0:
                valley[y,x] |= (WALL << UPDATE_SHIFT)
    valley = valley >> 8
    return valley

class DijkstraNode:
    def __init__(self, x, y, t, is_ground):
        self.x = x
        self.y = y
        self.t = t
        self.is_ground = is_ground
        self.value = 2**15
        self.neigbours = []
        self.back_neighbours = []
        self.prev = None

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return '[t={}, (x:{}, y:{})]'.format(self.t, self.x, self.y)

def create_graph(valley_states):
    pass

def calc_min_distance(valley_states, start_x, start_y, start_t, end_x, end_y): 
    end_nodes = []
    print('Creating nodes')
    all_nodes = [[[None for x in range(valley_states[0].shape[1])] for y in range(valley_states[0].shape[0])] for t in range(valley_states.shape[0])]
    for x in range(valley_states[0].shape[1]):
        for y in range(valley_states[0].shape[0]):
            for t in range(valley_states.shape[0]):
                n = DijkstraNode(x, y, t, valley_states[t][y,x] == 0)
                if n.is_ground:
                    if x == end_x and end_y == y:
                        end_nodes.append(n)
                    if x == start_x and y == start_y and t == start_t:
                        start_node = n
                        start_node.value = 0
                all_nodes[t][y][x] = n
    # Add edges
    print('Creating edges')
    for x in range(valley_states[0].shape[1]):
        for y in range(valley_states[0].shape[0]):
            for t in range(valley_states.shape[0]):
                n = all_nodes[t][y][x]
                if t+1 < valley_states.shape[0]:
                    if x != 0 and all_nodes[t+1][y][x-1].is_ground:
                        n.neigbours.append(all_nodes[t+1][y][x-1])
                    if x+1 < valley_states[0].shape[1] and all_nodes[t+1][y][x+1].is_ground:
                        n.neigbours.append(all_nodes[t+1][y][x+1])
                    if y != 0 and all_nodes[t+1][y-1][x].is_ground:
                        n.neigbours.append(all_nodes[t+1][y-1][x])
                    if y+1 < valley_states[0].shape[0] and all_nodes[t+1][y+1][x].is_ground:
                        n.neigbours.append(all_nodes[t+1][y+1][x])
                    n.neigbours.append(all_nodes[t+1][y][x])
    print('Finding shortest path')
    # Run Dijkstra's algorithm
    unchecked_nodes = []
    checked_nodes = set()
    heapq.heapify(unchecked_nodes)
    heapq.heappush(unchecked_nodes, (0, start_node))
    while len(unchecked_nodes) > 0:
        # print(len(unchecked_nodes))
        v, n = heapq.heappop(unchecked_nodes)
        if n not in checked_nodes:
            checked_nodes.add(n)
            for edge in n.neigbours:
                if edge not in checked_nodes and edge.is_ground and v + 1 < edge.value:
                       edge.value = v + 1
                       edge.prev = n
                       heapq.heappush(unchecked_nodes, (v + 1, edge))
    paths_found = [x.value!=2**15 for x in end_nodes]
    first_path_time = paths_found.index(True)
    best_end_node = end_nodes[first_path_time]
    return first_path_time


max_iter = 1000
INPUT_FILE = '24i.txt'
VALLY_STATES_FILE = INPUT_FILE+str(max_iter)+'.npy'
if not os.path.isfile(VALLY_STATES_FILE): 
    valley = create_valley_map(INPUT_FILE)
    
    valley_states = np.zeros([max_iter, valley.shape[0], valley.shape[1]])
    for t in range(max_iter):
        valley_states[t] = valley
        valley = advance_blizzards(valley)
        print(t)
    np.save(VALLY_STATES_FILE, np.array(valley_states))
else:
    valley_states = np.load(VALLY_STATES_FILE)

enter_x = 1
enter_y = 0
exit_x = valley_states[0].shape[1]-2
exit_y = valley_states[0].shape[0]-1
enter_to_exit_time = calc_min_distance(valley_states, start_x=enter_x, start_y=enter_y, start_t=0, end_x=exit_x, end_y=exit_y)
print(enter_to_exit_time)
exit_to_enter_time = calc_min_distance(valley_states, start_x=exit_x, start_y=exit_y, start_t=enter_to_exit_time, end_x=enter_x, end_y=enter_y)
print(exit_to_enter_time)
back_to_exit_time = calc_min_distance(valley_states, start_x=enter_x, start_y=enter_y, start_t=exit_to_enter_time, end_x=exit_x, end_y=exit_y)
print(back_to_exit_time)

from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time


MAP_WIDTH = 7
MAP_HEIGHT = 3500

shape_a = np.ones( (1, 4), dtype=np.uint8)
shape_b = np.array([[0,1,0],[1,0,1],[0,1,0]], dtype=np.uint8)
shape_c = np.array([[0,0,1],[0,0,1],[1,1,1]], dtype=np.uint8)
shape_d = np.ones( (4, 1), dtype=np.uint8)
shape_e = np.array( [[1,1],[1,1]], dtype=np.uint8)
shapes = [shape_a, shape_b, shape_c, shape_d, shape_e]
shapes_shade = [2,3,4,5,6]

with open('17i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
wind_string = lines[0]

last_highest_row = MAP_HEIGHT-1
block_map = np.zeros( (MAP_HEIGHT, MAP_WIDTH), dtype=np.uint8)
fig, ax = plt.subplots()
wind_index = 0
shape_index = 0
show_plot = False


def highest_free_row(block_map):
    global last_highest_row
    r = 0
    found = False
    while not found:
        row_sum = 0
        for c in range(block_map.shape[1]):
            row_sum += block_map[last_highest_row-r, c]
        if 0 == row_sum:
            found = True
            last_highest_row = last_highest_row-r
        r += 1
    return last_highest_row

def drop_shape_into_map(block_map, shape):
    y = highest_free_row(block_map)-2-shape.shape[0]
    for c in range(shape.shape[1]):
        for r in range(shape.shape[0]):
            block_map[r+y, c+2] = shape[r,c]
    return 2, y


def shape_can_move_left(block_map, shape, x, y):
    if x == 0:
        return False
    for c in range(shape.shape[1]):
        for r in range(shape.shape[0]):
            if shape[r,c] != 0:
                if block_map[y+r,x+c-1] >= 2:
                    return False
    return True


def shape_can_move_right(block_map, shape, x, y):
    if x+shape.shape[1] == MAP_WIDTH:
        return False
    for c in range(shape.shape[1]):
        for r in range(shape.shape[0]):
            if shape[r,c] != 0:
                if block_map[y+r,x+c+1] >= 2:
                    return False
    return True


def shape_can_move_down(block_map, shape, x, y):
    if y+shape.shape[0] == MAP_HEIGHT:
        return False
    for c in range(shape.shape[1]):
        for r in range(shape.shape[0]):
            if shape[r,c] != 0:
                if block_map[y+r+1,x+c] >= 2:
                    return False
    return True


def remove_shape(block_map, shape, x, y):
    for c in range(shape.shape[1]):
        for r in range(shape.shape[0]):
            if 0 != shape[r, c]:
                block_map[y+r,x+c] = 0


def draw_in_shape(block_map, shape, x, y, value):
    for c in range(shape.shape[1]):
        for r in range(shape.shape[0]):
            if 0 != shape[r, c]:
                block_map[y+r,x+c] = value


def move_shape_left(block_map, shape, x, y):
    remove_shape(block_map, shape, x, y)
    draw_in_shape(block_map, shape, x-1, y, 1)
    return (x-1, y)


def move_shape_right(block_map, shape, x, y):
    remove_shape(block_map, shape, x, y)
    draw_in_shape(block_map, shape, x+1, y, 1)
    return (x+1, y)

def move_shape_down(block_map, shape, x, y):
    remove_shape(block_map, shape, x, y)
    draw_in_shape(block_map, shape, x, y+1, 1)
    return (x, y+1)

def mark_as_stationary(block_map, shape, x, y, shade):
    remove_shape(block_map, shape, x, y)
    draw_in_shape(block_map, shape, x, y, shade)
    return (x, y)

def print_map(block_map):
    plt.imshow(block_map, cmap='CMRmap',interpolation='nearest')#,aspect='auto')
    plt.show()


def drop_shape(block_map, shape_index, wind_idx, frame):
    stationary = False
    s = shapes[shape_index]
    x, y = drop_shape_into_map(block_map, s)
    while not stationary:
        if wind_string[wind_idx%len(wind_string)] == '>':
            if shape_can_move_right(block_map, s, x, y):
                x, y = move_shape_right(block_map, s, x, y)
        else:
            if shape_can_move_left(block_map, s, x, y):
                x, y = move_shape_left(block_map, s, x, y)
        wind_idx += 1
        if frame == wind_idx:
            ax.clear()
            ax.imshow(block_map, cmap='Greys',interpolation='nearest')
        if shape_can_move_down(block_map, s, x, y):
            x, y = move_shape_down(block_map, s, x, y)
        else:
            stationary = True
            mark_as_stationary(block_map, s, x, y, shapes_shade[shape_index])
    return wind_idx 


def animate(frame):
    block_map = np.zeros( (MAP_HEIGHT, MAP_WIDTH), dtype=np.uint8)
    wind_index = 0
    shape_index = 0
    for i in range(frame):
        wind_index = drop_shape(block_map, shape_index, wind_index, frame)
        shape_index += 1
        shape_index %= len(shapes)


def row_is_equal(block_map, ya, yb):
    for c in range(block_map.shape[1]):
        if block_map[ya, c] != block_map[yb, c]:
            return False
    return True


def is_repetition(block_map, ya, yb):
    for i in range(100):
        if not row_is_equal(block_map, ya-i, yb-i):
            return False
    return True

def row_only_contains_shape_a(block_map, y):
    for c in range(block_map.shape[1]):
        if block_map[y, c] != 2 and block_map[y, c] != 0:
            return False
    return True


def find_repetition_cut(block_map, start_offset):
    start = block_map.shape[0]-start_offset
    for i in range(1, 3000):
        if is_repetition(block_map, start, start-i):
            if row_only_contains_shape_a(block_map, start):
                print('Repetition found: {}, {}, {}'.format(i, start, start-i))
                return (i, start, start-i)
    return (0,0,0)

def count_shapes_in_range(block_map, start_y, end_y):
    bit_count = 0
    shape_bit_weight_lookup = [0, 0, 0.25, 0.25, 0.2, 0.25, 0.25]
    for y in range(end_y,start_y):
        for c in range(block_map.shape[1]):
            bit_count += shape_bit_weight_lookup[block_map[y, c]]
    return int(round(bit_count))


# ============================================================================ #
#    Part 1
# ============================================================================ #
if show_plot:
    ani = FuncAnimation(fig, animate, frames=200, interval=100, repeat=False)
    plt.show()
else:
    start_time = time.time()
    for i in range(2022):
        wind_index = drop_shape(block_map, shape_index, wind_index,-1)
        shape_index += 1
        shape_index %= len(shapes)
        if i % 100 == 0:
            print(i)
    print('Part 1: {}'.format(block_map.shape[0]- highest_free_row(block_map)-1))
    print("--- %s seconds ---" % (time.time() - start_time))
    print_map(block_map)

# ============================================================================ #
#    Part 2
# ============================================================================ #

start_time = time.time()
MAP_HEIGHT = 7000
TOTAL_BLOCKS = 1000000000000
wind_index = 0
shape_index = 0
block_map = np.zeros( (MAP_HEIGHT, MAP_WIDTH), dtype=np.uint8)
last_highest_row = MAP_HEIGHT-1

for i in range(int(MAP_HEIGHT/2)):
    wind_index = drop_shape(block_map, shape_index, wind_index,-1)
    shape_index += 1
    shape_index %= len(shapes)
    if i % 100 == 0:
        print(i)
cut_found = False
i = 1
while not cut_found and i < 3000:
    print('--- {}\t ----'.format(i))
    repetition_length, first, second = find_repetition_cut(block_map, i)
    if 0 != repetition_length:
        cut_found = True
    else:
        i += 1
shapes_in_repetion = count_shapes_in_range(block_map, first, second)
height_before_repetition = MAP_HEIGHT-1-first
shapes_before_repetition = count_shapes_in_range(block_map, MAP_HEIGHT-1,first)
print('cut found at {} with {} number of shapes and hight {}'.format(first, shapes_in_repetion, repetition_length))
print('shapes before repetion: {} with height {}'.format(shapes_before_repetition, height_before_repetition))
print_map(block_map)
rep_count = int((TOTAL_BLOCKS-height_before_repetition)/shapes_in_repetion)
total_height = height_before_repetition + rep_count*repetition_length
print(total_height)

# Find height of shapes before repetion + the remainder shapes
wind_index = 0
shape_index = 0
block_map = np.zeros( (MAP_HEIGHT, MAP_WIDTH), dtype=np.uint8)
last_highest_row = MAP_HEIGHT-1
print(TOTAL_BLOCKS - rep_count*shapes_in_repetion)
for i in range(TOTAL_BLOCKS - rep_count*shapes_in_repetion):
    wind_index = drop_shape(block_map, shape_index, wind_index,-1)
    shape_index += 1
    shape_index %= len(shapes)
    if i % 100 == 0:
        print(i)
height_of_remainder_and_initial = block_map.shape[0]- highest_free_row(block_map)-1
print('Part 2: {}'.format(height_of_remainder_and_initial+rep_count*repetition_length))
print_map(block_map)
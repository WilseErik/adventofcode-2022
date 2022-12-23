from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time
import matplotlib.image

GROUND = 0
ELF = 32
PROPOSED_FROM_NORTH = 1
PROPOSED_FROM_SOUTH = 2
PROPOSED_FROM_WEST = 4
PROPOSED_FROM_EAST = 8
PROPOSE_MASK = 0x0f
one_elf_moved = False

def propose_moves(source_map, x, y, round_nbr):
    if source_map[y, x] != ELF:
        return
    if x < 2 or y < 2 or x > (MAP_WIDTH-3) or y > (MAP_HEIGHT-3):
        return
    north_pixels = [source_map[y-1, x-1], source_map[y-1, x], source_map[y-1, x+1]]
    south_pixels = [source_map[y+1, x-1], source_map[y+1, x], source_map[y+1, x+1]]
    west_pixels = [source_map[y-1, x-1], source_map[y, x-1], source_map[y+1, x-1]]
    east_pixels = [source_map[y-1, x+1], source_map[y, x+1], source_map[y+1, x+1]]
    n_pixels = list(map(lambda x:x&~PROPOSE_MASK, north_pixels))
    s_pixels = list(map(lambda x:x&~PROPOSE_MASK, south_pixels))
    w_pixels = list(map(lambda x:x&~PROPOSE_MASK, west_pixels))
    e_pixels = list(map(lambda x:x&~PROPOSE_MASK, east_pixels))
    all_neigbhours = n_pixels+s_pixels+w_pixels+e_pixels
    if all_neigbhours == [GROUND for i in range(4*3)]:
        return

    if 0 == (round_nbr%4):
        if n_pixels == [GROUND, GROUND, GROUND]:
            source_map[y-1, x] |= PROPOSED_FROM_SOUTH
        elif s_pixels == [GROUND, GROUND, GROUND]:
            source_map[y+1, x] |= PROPOSED_FROM_NORTH
        elif w_pixels == [GROUND, GROUND, GROUND]:
            source_map[y, x-1] |= PROPOSED_FROM_EAST
        elif e_pixels == [GROUND, GROUND, GROUND]:
            source_map[y, x+1] |= PROPOSED_FROM_WEST
    elif 1 == (round_nbr%4):
        if s_pixels == [GROUND, GROUND, GROUND]:
            source_map[y+1, x] |= PROPOSED_FROM_NORTH
        elif w_pixels == [GROUND, GROUND, GROUND]:
            source_map[y, x-1] |= PROPOSED_FROM_EAST
        elif e_pixels == [GROUND, GROUND, GROUND]:
            source_map[y, x+1] |= PROPOSED_FROM_WEST
        elif n_pixels == [GROUND, GROUND, GROUND]:
            source_map[y-1, x] |= PROPOSED_FROM_SOUTH
    elif 2 == (round_nbr%4):
        if w_pixels == [GROUND, GROUND, GROUND]:
            source_map[y, x-1] |= PROPOSED_FROM_EAST
        elif e_pixels == [GROUND, GROUND, GROUND]:
            source_map[y, x+1] |= PROPOSED_FROM_WEST
        elif n_pixels == [GROUND, GROUND, GROUND]:
            source_map[y-1, x] |= PROPOSED_FROM_SOUTH
        elif s_pixels == [GROUND, GROUND, GROUND]:
            source_map[y+1, x] |= PROPOSED_FROM_NORTH
    elif 3 == (round_nbr%4):
        if e_pixels == [GROUND, GROUND, GROUND]:
            source_map[y, x+1] |= PROPOSED_FROM_WEST
        elif n_pixels == [GROUND, GROUND, GROUND]:
            source_map[y-1, x] |= PROPOSED_FROM_SOUTH
        elif s_pixels == [GROUND, GROUND, GROUND]:
            source_map[y+1, x] |= PROPOSED_FROM_NORTH
        elif w_pixels == [GROUND, GROUND, GROUND]:
            source_map[y, x-1] |= PROPOSED_FROM_EAST

def performed_proposed_move(source_map, x, y):
    global one_elf_moved
    if source_map[y, x] & PROPOSE_MASK == PROPOSED_FROM_NORTH:
        source_map[y-1, x] = GROUND
        source_map[y, x] = ELF
        one_elf_moved = True
    elif source_map[y, x] & PROPOSE_MASK == PROPOSED_FROM_SOUTH:
        source_map[y+1, x] = GROUND
        source_map[y, x] = ELF
        one_elf_moved = True
    elif source_map[y, x] & PROPOSE_MASK == PROPOSED_FROM_WEST:
        source_map[y, x-1] = GROUND
        source_map[y, x] = ELF
        one_elf_moved = True
    elif source_map[y, x] & PROPOSE_MASK == PROPOSED_FROM_EAST:
        source_map[y, x+1] = GROUND
        source_map[y, x] = ELF
        one_elf_moved = True
    source_map[y, x] &= ~PROPOSE_MASK

def run_propose_stage(source_map, round_nbr):
    for r in range(MAP_HEIGHT):
        for c in range(MAP_WIDTH): 
            propose_moves(source_map, c, r, round_nbr)

def run_move_stage(source_map):
    for r in range(MAP_HEIGHT):
        for c in range(MAP_WIDTH): 
            performed_proposed_move(source_map, c, r)

def show_map(map_to_plot):
    plt.imshow(map_to_plot, cmap='gist_earth_r',interpolation='nearest')#,aspect='auto')
    plt.show()

def count_empty_ground(source_map):
    min_x, min_y = 2**15, 2**15
    max_x, max_y = 0, 0
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if source_map[y, x] == ELF:
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
    count = 0
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if source_map[y, x] == GROUND:
                count += 1
    return count

def load_map(map_lines):
    map_2d = np.ones((MAP_HEIGHT, MAP_WIDTH), dtype=np.uint8) * GROUND
    for y in range(len(map_lines)):
        for c in range(len(map_lines[0])):
            if map_lines[y][c] == '#':
                map_2d[y+SIDE_MARGIN,c+SIDE_MARGIN] = ELF
    return map_2d
# ============================================================================ #
#    Part 1
# ============================================================================ #

with open('23i.txt', 'r') as f:
    map_lines = [l.strip() for l in f.readlines()]

SIDE_MARGIN = 70
MAP_WIDTH = len(map_lines[0])+2*SIDE_MARGIN
MAP_HEIGHT = len(map_lines)+2*SIDE_MARGIN
map_2d = load_map(map_lines)

show_map(map_2d)
for i in range(10):
    run_propose_stage(map_2d, i)
    run_move_stage(map_2d)
print(count_empty_ground(map_2d))
show_map(map_2d)

# ============================================================================ #
#    Part 2
# ============================================================================ #

map_2d = load_map(map_lines)
show_map(map_2d)
i = 0
one_elf_moved = True
while one_elf_moved:
    start_time = time.time()
    one_elf_moved = False
    run_propose_stage(map_2d, i)
    run_move_stage(map_2d)
    i += 1
    print("--- %d, %s seconds ---" % (i, time.time() - start_time))
    if i%10 == 0:
        matplotlib.image.imsave('name{}.png'.format(i), map_2d)
show_map(map_2d)
print('Part 2: {}'.format(i))

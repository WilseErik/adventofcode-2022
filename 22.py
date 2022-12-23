import re

class Side:
    def __init__(self, lines, x, y):
        self.x = x
        self.y = y
        self.lines = lines.copy()
        self.neigbours = {'r':None, 'l':None, 'u':None, 'd':None}
        self.neigbour_rotation = {'r':0, 'r':1, 'r':2, 'r':3}
        self.width = len(lines)
        

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x*10000+self.y < (other.x*10000+other.y)

    def __repr__(self):
        return str((self.x, self.y))

# def get_side_from_list(side_list, x, y):
#     ret_val = None
#     for s in side_list:
#         if s.x == x and s.y == y:
#             ret_val = s
#     return ret_val

def get_side_using_block_pos(side_list, x, y, side_len):
    ret_val = None
    for s in side_list:
        if s.x == x*side_len and s.y == y*side_len:
            ret_val = s
    return ret_val

def find_x_neighbour(map_lines, x, y, shift):
    x_span = re.compile(r'[\.|#]+').search(map_lines[y]).span()
    neigbour_x = (((x - x_span[0]) + shift) % (x_span[1]-x_span[0])) + x_span[0]
    return (neigbour_x, y)

def find_y_neighbour(map_lines, x, y, shift):
    column_str = ''.join([map_lines[row][x] for row in range(len(map_lines))])
    y_span = re.compile(r'[\.|#]+').search(column_str).span()
    neigbour_y = (((y - y_span[0]) + shift) % (y_span[1]-y_span[0])) + y_span[0]
    return (x, neigbour_y)

def walk_staight(map_lines, x, y, heading, length):
    walk_done = False
    length_walked = 0
    while not walk_done and length_walked < length:
        if 0 == heading:
            nx, ny = find_x_neighbour(map_lines, x, y, 1)
        elif 1 == heading:
            nx, ny = find_y_neighbour(map_lines, x, y, 1)
        elif 2 == heading:
            nx, ny = find_x_neighbour(map_lines, x, y, -1)
        elif 3 == heading:
            nx, ny = find_y_neighbour(map_lines, x, y, -1)
        if map_lines[ny][nx] == '#':
            walk_done = True
        else:
            x = nx
            y = ny
            length_walked += 1
    return (x, y)

def run_path_command(map_lines, x, y, lengths, rotations):
    heading = 0
    for i in range(len(rotations)):
        x, y = walk_staight(map_lines, x, y, heading, lengths[i])
        if rotations[i] == 'R':
            heading = (heading + 1) % 4
        else:
            heading = (heading - 1) % 4
    x, y = walk_staight(map_lines, x, y, heading, lengths[-1])
    return (x+1,y+1,heading)

def walk_step_on_cube(side, x, y, heading):
    nside = side
    if heading == 0: # moving right
        if x+1 == side.width:
            nside = side.neigbours['r']
            if side.neigbour_rotation['r'] == 0:
                # heading is right
                nx = 0
                ny = y
            elif side.neigbour_rotation['r'] == 1:
                # heading is down
                nx = side.width-1 - y
                ny = 0
            elif side.neigbour_rotation['r'] == 2:
                # heading is left
                nx = side.width - 1
                ny = side.width - 1 - y
            else:
                # heading is up
                nx = y
                ny = side.width - 1
            if side.neigbours['r'].lines[ny][nx] != '#':
                x = nx
                y = ny
                heading = side.neigbour_rotation['r']
        else:
            if side.lines[y][x+1] != '#':
                x += 1
    elif heading == 1: # moving down
        if y == 0:
            nside = side.neigbours['d']
            if side.neigbour_rotation['d'] == 0:
                # heading is down
                nx = x
                ny = 0
            elif side.neigbour_rotation['d'] == 1:
                # heading is left
                nx = side.width - 1
                ny = x
            elif side.neigbour_rotation['d'] == 2:
                # heading is up
                nx = side.width - 1 - x
                ny = side.width - 1
            else:
                # heading is right
                nx = 0
                ny = x
            if side.neigbours['d'].lines[ny][nx] != '#':
                x = nx
                y = ny
                heading = side.neigbour_rotation['d']
        else:
            if side.lines[y-1][x] != '#':
                y -= 1
    elif heading == 2: # moving left
        if x == 0:
            nside = side.neigbours['l']
            if side.neigbour_rotation['l'] == 0:
                # heading is left
                nx = side.width - 1
                ny = y
            elif side.neigbour_rotation['l'] == 1:
                # heading is up
                nx = side.width - 1 - x
                ny = side.width - 1
            elif side.neigbour_rotation['l'] == 2:
                # heading is right
                nx = side.width - 1
                ny = side.width - 1 - y
            else:
                # heading is down
                nx = y
                ny = 0
            if side.neigbours['l'].lines[ny][nx] != '#':
                x = nx
                y = ny
                heading = (2 + side.neigbour_rotation['l']) % 4
        else:
            if side.lines[y][x-1] != '#':
                x -= 1
    elif heading == 3: # moving up
        if y+1 == side.width:
            nside = side.neigbours['u']
            if side.neigbour_rotation['u'] == 0:
                # heading is up
                nx = x
                ny = side.width-1
            elif side.neigbour_rotation['u'] == 1:
                # heading is right
                nx = 0
                ny = x
            elif side.neigbour_rotation['u'] == 2:
                # heading is down
                nx = side.width - 1 - x
                ny = 0
            else:
                # heading is left
                nx = y
                ny = side.width - 1
            if side.neigbours['u'].lines[ny][nx] != '#':
                x = nx
                y = ny
                heading = side.neigbour_rotation['u']
        else:
            if side.lines[y+1][x] != '#':
                y += 1
    return nside, x, y, heading


def run_cube_path_command(sides, side, x, y, lengths, rotations):
    heading = 0
    for i in range(len(rotations)):
        for k in range(lengths[i]):
            side, x, y, heading = walk_step_on_cube(side, x, y, heading)
        if rotations[i] == 'R':
            heading = (heading + 1) % 4
        else:
            heading = (heading - 1) % 4
    for k in range(lengths[-1]):
        side, x, y, heading = walk_step_on_cube(side, x, y, heading)
    return (side.x+x+1,side.y+y+1,heading)

# ============================================================================ #
#    Part 1
# ============================================================================ #

with open('22ia.txt', 'r') as f:
    lines = [l.strip('\n\r') for l in f.readlines()]
raw_map_lines = [l for l in lines if ('.' in l or '#' in l)]
path_line = [l for l in lines if 'L' in l][0]
map_width = max(map(len, raw_map_lines))
map_lines = [l + ''.join([' ' for i in range(map_width-len(l))]) for l in raw_map_lines]
path_lengths = [int(s) for s in re.split(r'[\D]+', path_line) if len(s) != 0]
path_directions = [s for s in re.split(r'[\d]+', path_line) if len(s) != 0]
start_x = re.search(r'[\.|#]', map_lines[0]).start()
x, y, heading = run_path_command(map_lines, start_x, 0, path_lengths, path_directions)
print((x, y, heading))
print('Part 1: {}'.format(y*1000+4*x+heading))

# ============================================================================ #
#    Part 2
# ============================================================================ #

example_data = True
if example_data:
    SIDE_LENGTH = 4
sides = []

for side_row in range(int(len(map_lines)/SIDE_LENGTH)):
    for side_col in range(int(len(map_lines[0])/SIDE_LENGTH)):
        side_x = side_col*SIDE_LENGTH
        side_y = side_row*SIDE_LENGTH
        if map_lines[side_y][side_x] != ' ':
            side_lines = [map_lines[r][side_x:side_x+SIDE_LENGTH] for r in range(side_y, side_y+SIDE_LENGTH)]
            sides.append(Side(side_lines, side_x, side_y))

# Always start on top
if example_data:
    top = get_side_using_block_pos(sides, 2, 0, SIDE_LENGTH)
    front = get_side_using_block_pos(sides, 2, 1, SIDE_LENGTH)
    bottom = get_side_using_block_pos(sides, 2, 2, SIDE_LENGTH)
    left = get_side_using_block_pos(sides, 1, 1, SIDE_LENGTH)
    back = get_side_using_block_pos(sides, 0, 1, SIDE_LENGTH)
    right = get_side_using_block_pos(sides, 3, 2, SIDE_LENGTH)
    
    top.neigbours = {'r':right, 'l':left, 'u':back, 'd':front}
    top.neigbour_rotation = {'r':2, 'l':3, 'u':2, 'd':0}
    front.neigbours = {'r':right, 'l':left, 'u':top, 'd':bottom}
    front.neigbour_rotation = {'r':1, 'l':0, 'u':0, 'd':0}
    bottom.neigbours = {'r':right, 'l':left, 'u':front, 'd':back}
    bottom.neigbour_rotation = {'r':0, 'l':1, 'u':0, 'd':2}
    left.neigbours = {'r':front, 'l':back, 'u':top, 'd':bottom}
    left.neigbour_rotation = {'r':0, 'l':0, 'u':1, 'd':3}
    back.neigbours = {'r':left, 'l':right, 'u':top, 'd':bottom}
    back.neigbour_rotation = {'r':0, 'l':1, 'u':2, 'd':2}
    right.neigbours = {'r':top, 'l':bottom, 'u':front, 'd':back}
    right.neigbour_rotation = {'r':2, 'l':0, 'u':3, 'd':1}

print(top)
print(front)
print(bottom)
print(left)
print(back)
print(right)

x, y, heading = run_cube_path_command(map_lines, top, 0, 0, path_lengths, path_directions)
print((x, y, heading))
print('Part 1: {}'.format(y*1000+4*x+heading))


# for s in sides:
#     if s.left_neighbour is None:
#         left = get_side_from_list(sides, s.x-SIDE_LENGTH, s.y)    
#         if left is not None:
#             s.left_neighbour = left
#             left.right_neighbour = s

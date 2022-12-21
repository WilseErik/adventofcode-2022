import numpy as np

def count_surface_sides(box, x, y, z, surface_value=0):
    count = 0
    neigbours = [[x+1,y,z], [x-1,y,z], [x,y+1,z], [x,y-1,z], [x,y,z+1], [x,y,z-1]]
    for n in neigbours:
        if box[n[0], n[1], n[2]] == surface_value:
            count += 1
    return count


def is_in_box(box, point):
    inside = True
    if (point[0] < 0) or (point[1] < 0) or (point[2] < 0):
        inside = False
    if (point[0] >= box.shape[0]) or (point[1] >= box.shape[0]) or (point[2] >= box.shape[0]):
        inside = False
    return inside


def flood_with_water(box):
    edge_nodes = [[0,0,0]]
    WATER = 2
    while len(edge_nodes) != 0:
        next_edge_nodes = []
        for n in edge_nodes:
            x, y, z = n[0], n[1], n[2]
            box[x,y,z] = WATER
            neigbours = [[x+1,y,z], [x-1,y,z], [x,y+1,z], [x,y-1,z], [x,y,z+1], [x,y,z-1]]
            for neigh in neigbours:
                if (is_in_box(box, neigh) and
                    box[neigh[0], neigh[1], neigh[2]] == 0 and
                    neigh not in next_edge_nodes):
                    next_edge_nodes.append(neigh)
        edge_nodes = next_edge_nodes

# ============================================================================ #
#    Part 1
# ============================================================================ #

with open('18i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
blocks = [list(map(int, l.split(','))) for l in lines]

BOX_SIZE = 25
BOX_CENTER = 12
box = np.zeros((BOX_SIZE,BOX_SIZE, BOX_SIZE), dtype=np.uint8)

for b in blocks:
    x = b[0]+1
    y = b[1]+1
    z = b[2]+1
    box[x,y,z] = 1

surface = 0
for x in range(BOX_SIZE):
    for y in range(BOX_SIZE):
        for z in range(BOX_SIZE):
            if box[x,y,z] == 1:
                surface += count_surface_sides(box, x, y, z)
print('Part 1: {}'.format(surface))

# ============================================================================ #
#    Part 2
# ============================================================================ #

flood_with_water(box)
surface_to_water = 0
for x in range(BOX_SIZE):
    for y in range(BOX_SIZE):
        for z in range(BOX_SIZE):
            if box[x,y,z] == 1:
                surface_to_water += count_surface_sides(box, x, y, z, 2)
print('Part 2: {}'.format(surface_to_water))

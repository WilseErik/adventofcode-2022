from matplotlib import pyplot as plt
import numpy as np

SAND_VALUE = 150
ROCK_VALUE = 255
BACKGROUND_VALUE = 30
KILL_FLOOR = 190
MAP_WIDTH = 1000
MAP_HEIGHT = 200
SAND_SOURCE_X = 500
MAP_OFFSET_X = 0

class RockMap:
    def __init__(self):
        with open('14i.txt', 'r') as f:
            lines = [l.strip() for l in f.readlines()]
        self.shapes = []
        for line in lines:
            coord_strs = line.split(' -> ')
            self.shapes.append([{'x':int(coord.split(',')[0])-MAP_OFFSET_X, 'y':int(coord.split(',')[1])} for coord in coord_strs])
        self.rock_map = np.zeros( (MAP_WIDTH,MAP_HEIGHT), dtype=np.uint8)
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                self.set_background_pixel(x, y)
        for shape in self.shapes:
            self.fill_in_shape(shape)

    def fill_in_shape(self, shape):
        for i in range(len(shape)-1):
            point_a = shape[i]
            point_b = shape[i+1]
            if point_a['x'] == point_b['x']:
                x = point_a['x']
                if point_a['y'] < point_b['y']:
                    for y in range(point_a['y'], point_b['y']+1):
                        self.rock_map[x, y] = ROCK_VALUE
                else:
                    for y in range(point_b['y'], point_a['y']+1):
                        self.rock_map[x, y] = ROCK_VALUE
            elif point_a['y'] == point_b['y']:
                y = point_a['y']
                if point_a['x'] < point_b['x']:
                    for x in range(point_a['x'], point_b['x']+1):
                        self.rock_map[x, y] = ROCK_VALUE
                else:
                    for x in range(point_b['x'], point_a['x']+1):
                        self.rock_map[x, y] = ROCK_VALUE


    def fill_in_floor(self, level):
        for x in range(MAP_WIDTH):
            self.rock_map[x, level] = ROCK_VALUE


    def set_background_pixel(self, x, y):
        if (x+y) % 2:
            self.rock_map[x, y] = BACKGROUND_VALUE
        else:
            self.rock_map[x, y] = 0


    def drop_in_sand(self, ):
        self.rock_map[SAND_SOURCE_X-MAP_OFFSET_X, 0] = SAND_VALUE
        return (SAND_SOURCE_X-MAP_OFFSET_X, 0)


    def move_sand_grain(self, x, y, diff_x, diff_y):
        self.set_background_pixel(x, y)
        self.rock_map[x+diff_x, y+diff_y] = SAND_VALUE
        return (x+diff_x, y+diff_y)


    def update_sand_grain_position(self, grain_x, grain_y):
        new_x = grain_x
        new_y = grain_y
        if self.rock_map[grain_x, grain_y + 1] < SAND_VALUE:
            new_x, new_y = self.move_sand_grain(grain_x, grain_y, 0, 1)
        elif self.rock_map[grain_x-1, grain_y+1] < SAND_VALUE:
            new_x, new_y = self.move_sand_grain(grain_x, grain_y, -1, 1)
        elif self.rock_map[grain_x+1, grain_y+1] < SAND_VALUE:
            new_x, new_y = self.move_sand_grain(grain_x, grain_y, 1, 1)
        return (new_x, new_y)


    def pour_sand_grain(self):
        x, y = self.drop_in_sand()
        done = False
        while not done:
            last_x = x
            last_y = y
            x, y = self.update_sand_grain_position(x, y)
            if (y == last_y) or (y > KILL_FLOOR):
                done = True
        return (not (y > KILL_FLOOR), x, y)


    def find_lowest_shape(self):
        highest = 0
        for shape in self.shapes:
            for point in shape:
                if point['y'] > highest:
                    highest = point['y']
        return highest


rock_map = RockMap()
grain_count = 0
while rock_map.pour_sand_grain()[0]:
    grain_count += 1

print('Part 1: {}'.format(grain_count))
plt.imshow(rock_map.rock_map.transpose(), cmap='Greys',interpolation='nearest')
plt.show()

rock_map = RockMap()
rock_map.fill_in_floor(rock_map.find_lowest_shape() + 2)
full = False
grain_count = 0
while not full:
    alive, x, y = rock_map.pour_sand_grain()
    grain_count += 1
    if y == 0 or not alive:
        full = True
print('Part 2: {}'.format(grain_count))
plt.imshow(rock_map.rock_map.transpose(), cmap='Greys',interpolation='nearest')
plt.show()

import re

class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def __hash__(self):
        return hash(repr(self))


class Sensor:
    def __init__(self, position, beacon_pos):
        self.position = position
        self.beacon_position = beacon_pos
        self.beacon_distance = manhattan_distance(self.position, self.beacon_position)


def manhattan_distance(a, b):
    return abs(a.x-b.x)+abs(a.y-b.y)


def pos_can_not_be_beacon(position, sensors, beacons):
    blocked = '.'
    for sensor in sensors:
        if manhattan_distance(position, sensor.position) <= sensor.beacon_distance:
            if position not in beacons:
                blocked = '#'
            else:
                blocked = 'B'
    return blocked


def range_blocked_by_sensor(y, sensor):
    if sensor.beacon_distance < manhattan_distance(Pair(sensor.position.x, y), sensor.position):
        r = []
    else:
        w = sensor.beacon_distance - abs(sensor.position.y-y)
        r = [sensor.position.x-w,sensor.position.x+w]
    return r


def range_contains(a, b):
    return (a[0] <= b[0]) and (b[1] <= a[1])


def range_overlaps(a, b):
    return (a[0] <= b[0]) and (a[1] >= b[0]) or (a[0] >= b[0]) and (a[1] >= b[0])


def range_follows(a, b):
    return (a[0] < b[0]) and (a[1]+1 == b[0])


def range_blocked_by_all_sensors(y, sensors, xy_limit):
    range_blocked_per_sensor = [range_blocked_by_sensor(y, s) for s in sensors]
    range_list = [r for r in range_blocked_per_sensor if len(r) != 0]
    for r in range_list:
        if r[0] < 0:
            r[0] = 0
        if r[1] < 0:
            r[1] = 0
        if r[0] > xy_limit:
            r[0] = xy_limit
        if r[1] > xy_limit:
            r[1] = xy_limit
    overlap = True
    while overlap:
        overlap = False
        for i in range(len(range_list)-1):
            for k in range(i+1, len(range_list)):
                if not overlap:
                    a = range_list[i]
                    b = range_list[k]
                    if range_contains(a, b):
                        overlap = True
                        range_list.remove(b)
                    elif range_contains(b, a):
                        overlap = True
                        range_list.remove(a)
                    elif range_overlaps(a, b):
                        overlap = True
                        if a[0] < b[0]:
                            a[1] = b[1]
                        else:
                            a[0] = b[0]
                        range_list.remove(b)
                    elif range_follows(a, b):
                        overlap = True
                        a[1] = b[1]
                        range_list.remove(b)
                    elif range_follows(b, a):
                        overlap = True
                        a[0] = b[0]
                        range_list.remove(b)

    return range_list


with open('15i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
sensors = []
for line in lines:
    parsed = re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', line)
    sensors.append(Sensor(Pair(int(parsed[0]), int(parsed[1])), Pair(int(parsed[2]), int(parsed[3]))))
beacons = set()
for sensor in sensors:
    beacons.add(sensor.beacon_position)

# ==============================================================================
# Part 1
# ==============================================================================
run_part_1 = False

if run_part_1:
    min_x, max_x = 0,0
    for s in sensors:
        if s.position.x - s.beacon_position.x < min_x:
            min_x = s.position.x - s.beacon_position.x
        if s.position.x + s.beacon_position.x > max_x:
            max_x = s.position.x + s.beacon_position.x
    print(min_x)
    print(max_x)
    a = [pos_can_not_be_beacon(Pair(x, 2000000), sensors, beacons) for x in range(min_x, max_x+1)]
    print(a.count('#'))

# ==============================================================================
# Part 2
# ==============================================================================
run_part_2 = True

if run_part_2:
    xy_range = 4000000
    #xy_range = 20
    for y in range(xy_range):
        if y % (xy_range/1000) == 0:
            print('Progress = {} %'.format(100.0*y/(xy_range)))
        r = range_blocked_by_all_sensors(y, sensors, xy_range)
        if r != [[0, xy_range]]:
            print(y)
            print(r)
            print('Answer = ' + str(y+4000000*(r[0][1]+1)))

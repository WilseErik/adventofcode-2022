import re
import time


class Blueprint:
    def __init__(self, line):
        fields = list(map(int, re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', line)))
        self.id = fields[0]
        self.ore_robot_ore_cost = fields[1]
        self.clay_robot_ore_cost = fields[2]
        self.obisdian_robot_ore_cost = fields[3]
        self.obisdian_robot_clay_cost = fields[4]
        self.geode_robot_ore_cost = fields[5]
        self.geode_robot_obsidian_cost = fields[6]
        print(fields)

class Player:
    def __init__(self, blueprint, resources=[0, 0, 0, 0], robots=[1, 0, 0, 0],time=0):
        self.resources = resources
        self.robots = robots
        self.blueprint = blueprint
        self.time = time

    def __repr__(self):
        return str(self.resources)+str(self.robots)+str(self.time)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.resources == other.resources and self.robots == other.robots

    def copy(self):
        state = Player(self.blueprint, self.resources.copy(), self.robots.copy(), self.time)
        return state

    def can_buy_ore_robot(self):
        return self.resources[0] >= self.blueprint.ore_robot_ore_cost

    def can_buy_clay_robot(self):
        return self.resources[0] >= self.blueprint.clay_robot_ore_cost

    def can_buy_obsidian_robot(self):
        return ((self.resources[0] >= self.blueprint.obisdian_robot_ore_cost) and
            (self.resources[1] >= self.blueprint.obisdian_robot_clay_cost))

    def can_buy_geode_robot(self):
        return ((self.resources[0] >= self.blueprint.geode_robot_ore_cost) and
            (self.resources[2] >= self.blueprint.geode_robot_obsidian_cost))

    def buy_ore_robot(self):
        self.resources[0] -= self.blueprint.ore_robot_ore_cost
        self.robots[0] += 1

    def buy_clay_robot(self):
        self.resources[0] -= self.blueprint.clay_robot_ore_cost
        self.robots[1] += 1

    def buy_obsidian_robot(self):
        self.resources[0] -= self.blueprint.obisdian_robot_ore_cost
        self.resources[1] -= self.blueprint.obisdian_robot_clay_cost
        self.robots[2] += 1

    def buy_geode_robot(self):
        self.resources[0] -= self.blueprint.geode_robot_ore_cost
        self.resources[2] -= self.blueprint.geode_robot_obsidian_cost
        self.robots[3] += 1

    def run_robots(self):
        self.resources[0] += self.robots[0]
        self.resources[1] += self.robots[1]
        self.resources[2] += self.robots[2]
        self.resources[3] += self.robots[3]

    def pass_time(self):
        self.time += 1


visited_states = set()
total_calls = 0
max_geodes = -1
def depth_first_search(player):
    global total_calls
    global visited_states
    global max_geodes
    total_calls += 1
    TIME_LIMIT = 32 #  use 24 for part 1
    if player.time==TIME_LIMIT:
        return player.resources[3]
    if player.resources[3] + (TIME_LIMIT-player.time)*(player.robots[3]+(TIME_LIMIT-player.time-1)) <= max_geodes:
        return -1
    hash_value = player.__hash__()
    if hash_value in visited_states:
        return -1
    visited_states.add(hash_value)
    geode_counts = -1
    if player.can_buy_ore_robot():
        p = player.copy()
        p.run_robots()
        p.buy_ore_robot()
        p.pass_time()
        new_count = depth_first_search(p)
        if new_count > geode_counts:
            geode_counts = new_count
    if player.can_buy_clay_robot():
        p = player.copy()
        p.run_robots()
        p.buy_clay_robot()
        p.pass_time()
        new_count = depth_first_search(p)
        if new_count > geode_counts:
            geode_counts = new_count
    if player.can_buy_obsidian_robot():
        p = player.copy()
        p.run_robots()
        p.buy_obsidian_robot()
        p.pass_time()
        new_count = depth_first_search(p)
        if new_count > geode_counts:
            geode_counts = new_count
    if player.can_buy_geode_robot():
        p = player.copy()
        p.run_robots()
        p.buy_geode_robot()
        p.pass_time()
        new_count = depth_first_search(p)
        if new_count > geode_counts:
            geode_counts = new_count
    p = player.copy()
    p.run_robots()
    p.pass_time()
    new_count = depth_first_search(p)
    if new_count > geode_counts:
            geode_counts = new_count
    if geode_counts > max_geodes:
        max_geodes = geode_counts
    return geode_counts


with open('19i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
blueprints = [Blueprint(l) for l in lines]
quality_levels = []
for i in range(3): #  loop through all for part 1
    b = blueprints[i]
    start_time = time.time()
    visited_states = set()
    total_calls = 0
    max_geodes = -1
    collected_geodes = depth_first_search(Player(b))
    quality_levels.append(collected_geodes*b.id)
    print('ID: {}, geodes: {}, total_calls: {}'.format(b.id, collected_geodes, total_calls))
    print("--- %s seconds ---" % (time.time() - start_time))
print('quality_levels')
print(quality_levels)
print(sum(quality_levels))

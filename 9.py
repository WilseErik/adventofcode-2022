class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x += x
        self.y += y

    def copy(self):
        return Pair(self.x, self.y)

    def __repr__(self):
        return '({:}, {:})'.format(self.x, self.y)

    def __eq__(self, other):
        return (self.x==other.x) and (self.y==other.y)

    def is_touching(self, point):
        return ((abs(self.x-point.x) <= 1) and (abs(self.y-point.y) <= 1))

def update_tail(head, tail):
    if not head.is_touching(tail):
        if head.x > tail.x:
            tail.x += 1
        elif head.x < tail.x:
            tail.x -= 1
        if head.y > tail.y:
            tail.y += 1
        elif head.y < tail.y:
            tail.y -= 1

with open('9i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
motion_dict = {'R':Pair(1, 0), 'L':Pair(-1, 0), 'U':Pair(0, 1), 'D':Pair(0, -1)}
motions = []
for line in lines:
    for i in range(int(line.split()[1])):
        motions.append(motion_dict[line.split()[0]])
knots = [Pair(0, 0) for i in range(10)]
visited_points = [knots[-1].copy()]
for m in motions:
    knots[0].move(m.x, m.y)
    for i in range(len(knots)-1):
        update_tail(knots[i], knots[i+1])
    if knots[-1] not in visited_points:
        visited_points.append(knots[-1].copy())
print(len(visited_points))

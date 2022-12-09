with open('5i.txt', 'r') as f:
    lines = f.readlines()
def_lines = [l for l in lines if '[' in l]
cmd_lines = [l for l in lines if 'move' in l]
piles = [[] for i in range(int(len(def_lines[-1])/4))]
for i in range(len(def_lines)):
    for k in range(len(piles)):
        box = def_lines[-1-i][4*k+1:4*k+2]
        if ' ' != box:
            piles[k].append(box)
commands = [[int(l.split()[1]), int(l.split()[3])-1, int(l.split()[5])-1] for l in cmd_lines]
for cmd in commands:
    popped = [piles[cmd[1]].pop() for i in range(cmd[0])]
    for i in range(cmd[0]):
        piles[cmd[2]].append(popped[-1-i])
print(''.join([p.pop() for p in piles]))

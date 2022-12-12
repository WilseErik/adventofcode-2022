with open('10i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
x_list = [1, 1]
x = 1
for line in lines:
    if 'addx' in line:
        x_list.append(x)
        x += int(line.split()[1])
        x_list.append(x)
    elif 'noop' in line:
        x_list.append(x)
# Part 1
indicies = [20, 60, 100, 140, 180, 220]
print(sum([x_list[idx]*idx for idx in indicies]))
# Part 2
for r in range(6):
    row_pixels = [' ' for i in range(40)]
    for c in range(40):
        x = x_list[r*40 + c+1]
        if (((c-1) <= x) and (x <= c+1)):
            row_pixels[c] = '#'
    print(''.join(row_pixels))
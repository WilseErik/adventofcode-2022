with open('1i.txt', 'r') as f:
    lines = f.readlines()
calories = [0]
elf = 0
for line in lines:
    if 0 == len(line.strip()):
        elf += 1
        calories.append(0)
    else:
        calories[elf] += int(line.strip())
print(max(calories))
calories.sort()
print(sum(calories[-3:]))
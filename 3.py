def common_chars(str_a, str_b):
    common = []
    for c in str_a:
        if c in str_b and c not in common:
            common.append(c)
    return common

def get_prio(character):
    if character.isupper():
        return (27 + ord(character) - ord('A'))
    else:
        return (1 + ord(character) - ord('a'))

with open('3i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
prio_sum = 0 # Part 1
for line in lines:
    comp_len = int(len(line)/2)
    prio_sum += get_prio(common_chars(line[:comp_len], line[comp_len:])[0])
print(prio_sum)
prio_sum = 0 # Part 2
for i in range(int(len(lines)/3)):
    c = common_chars(lines[i*3+2], ''.join(common_chars(lines[i*3+0], lines[i*3+1])))[0]
    prio_sum += get_prio(c)
print(prio_sum)
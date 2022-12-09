def is_in_range(x, low, high):
    return ((x >= low) and (x <= high))

with open('4i.txt', 'r') as f:
    lines = [l.strip().replace('-', ',').split(',') for l in f.readlines()]
contained_pairs, overlapping_pairs = 0, 0
for line in lines:
    a_low, a_high, b_low, b_high = int(line[0]), int(line[1]), int(line[2]), int(line[3])
    if ((a_low >= b_low) and (a_high <= b_high)) or ((a_low <= b_low) and (a_high >= b_high)):
        contained_pairs += 1
    if (is_in_range(a_low, b_low, b_high) or is_in_range(a_high, b_low, b_high)):
        overlapping_pairs += 1
    elif (is_in_range(b_low, a_low, a_high) or is_in_range(b_high, a_low, a_high)):
        overlapping_pairs += 1
print(contained_pairs)
print(overlapping_pairs)
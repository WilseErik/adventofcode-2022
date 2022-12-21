class Entry:
    def __init__(self, x):
        self.y = x

    def __repr__(self):
        return str(self.y)


def mix(file, original):
    decrypted = file.copy()
    for entry in original:
        entry_index = decrypted.index(entry)
        new_index = (entry_index+entry.y)%(len(file)-1)
        if new_index != 0:
            decrypted.insert(new_index, decrypted.pop(entry_index))
        else:
            decrypted.append(decrypted.pop(entry_index))
    return decrypted

# ============================================================================ #
#    Part 1
# ============================================================================ #

with open('20i.txt', 'r') as f:
    file = [Entry(int(l.strip())) for l in f.readlines()]
for e in file:
    if '0' == str(e):
        zero_entry = e
file_length = len(file)
mixed_file = mix(file, file)
index_of_zero = mixed_file.index(zero_entry)
result = [mixed_file[(index_of_zero+x)%file_length].y for x in [1000,2000,3000]]
print(result)
print('Part 1: ' + str(sum(result)))

# ============================================================================ #
#    Part 2
# ============================================================================ #
decyption_key = 811589153
for e in file:
    e.y *= decyption_key
mixed_file = file.copy()
for i in range(10):
    mixed_file = mix(mixed_file, file)
index_of_zero = mixed_file.index(zero_entry)
result = [mixed_file[(index_of_zero+x)%file_length].y for x in [1000,2000,3000]]
print(result)
print('Part 2: ' + str(sum(result)))

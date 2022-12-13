import re
from functools import cmp_to_key

def string_to_list(string):
    if '[]' == string:
        return []
    if string[0] != '[':
        return int(re.findall(r'\d+', string)[0])
    else:
        index = 1
        brace_level = 1
        str_elements = ['']
        while brace_level > 0:
            if '[' == string[index]:
                str_elements[-1] += '['
                brace_level += 1
            elif ']' == string[index]:
                brace_level -= 1
                if 0 != brace_level:
                    str_elements[-1] += ']'
            elif ',' == string[index] and brace_level == 1:
                str_elements.append('')
            else:
                str_elements[-1] += string[index]
            index += 1
        result_list = [string_to_list(e) for e in str_elements]
        return result_list

def compare_list(list_a, list_b):
    min_len = min([len(list_a), len(list_b)])
    done = False
    idx = 0
    result = 0
    while not done and (idx < min_len):
        if isinstance(list_a[idx], int) and isinstance(list_b[idx], int):
            if list_a[idx] == list_b[idx]:
                idx += 1
            else:
                done = True
                result = list_a[idx] - list_b[idx]
        elif isinstance(list_a[idx], list) and isinstance(list_b[idx], list):
            comp = compare_list(list_a[idx], list_b[idx])
            if 0 == comp:
                idx += 1
            else:
                result = comp
                done = True
        elif isinstance(list_a[idx], list) and isinstance(list_b[idx], int):
            comp = compare_list(list_a[idx], [list_b[idx]])
            if 0 == comp:
                idx += 1
            else:
                result = comp
                done = True
        elif isinstance(list_a[idx], int) and isinstance(list_b[idx], list):
            comp = compare_list([list_a[idx]], list_b[idx])
            if 0 == comp:
                idx += 1
            else:
                result = comp
                done = True
    if not done:
        result = len(list_a) - len(list_b)
    return result

with open('13i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]

# Part 1
list_pairs = [[string_to_list(lines[i*3]), string_to_list(lines[i*3+1])] for i in range(int((len(lines)+1)/3))]
indicies_in_correct_order = []
for i in range(len(list_pairs)):
    pair = list_pairs[i]
    if compare_list(pair[0], pair[1]) < 0:
        indicies_in_correct_order.append(i+1)
print('Part 1: ' + str(sum(indicies_in_correct_order)))

# Part 2
divider_packet_2 = string_to_list('[[2]]')
divider_packet_6 = string_to_list('[[6]]')
all_lists = [divider_packet_2, divider_packet_6]
for pair in list_pairs:
    all_lists.append(pair[0])
    all_lists.append(pair[1])
all_lists = sorted(all_lists, key=cmp_to_key(compare_list))
print('Part 2: ' + str((all_lists.index(divider_packet_2)+1) * (all_lists.index(divider_packet_6)+1)))

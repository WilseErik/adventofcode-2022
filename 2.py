score_table_a = {
    'A X':3+1, 'A Y':6+2, 'A Z':0+3,
    'B X':0+1, 'B Y':3+2, 'B Z':6+3,
    'C X':6+1, 'C Y':0+2, 'C Z':3+3}
score_table_b = {
    'A X':0+3, 'A Y':3+1, 'A Z':6+2,
    'B X':0+1, 'B Y':3+2, 'B Z':6+3,
    'C X':0+2, 'C Y':3+3, 'C Z':6+1}
with open('2i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
print('part 1: {:}'.format(sum([score_table_a[line] for line in lines])))
print('part 2: {:}'.format(sum([score_table_b[line] for line in lines])))
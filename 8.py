def update_is_visible(array, row, col, limit):
    if array[row][col]['height'] > limit:
        limit = array[row][col]['height']
        array[row][col]['visible'] = 1
    return limit

def calc_scenic_score(array, row, col):
    scores = {'left':0, 'right':0, 'up':0, 'down':0}
    base_height = array[row][col]['height']
    done = {'left':False, 'right':False, 'up':False, 'down':False}
    for r in range(row+1, len(array)):
        if not done['down']:
            scores['down'] += 1
            if (array[r][col]['height'] >= base_height):
                done['down'] = True
    for r in range(row):
        if not done['up']:
            scores['up'] += 1
            if (array[row-r-1][col]['height'] >= base_height):
                done['up'] = True
    for c in range(col+1, len(array[0])):
        if not done['right']:
            scores['right'] += 1
            if (array[row][c]['height'] >= base_height):
                done['right'] = True
    for c in range(col):
        if not done['left']:
            scores['left'] += 1
            if (array[row][col-c-1]['height'] >= base_height):
                done['left'] = True
    return (scores['left']*scores['right']*scores['up']*scores['down'])

with open('8i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
rows = [[] for line in lines]
for i in range(len(lines)):
    rows[i] = [{'height':int(c), 'visible':0} for c in lines[i]]
row_count, col_count = len(rows), len(rows[0])
for r in range(row_count):
    highest_from_left, highest_from_right = -1, -1
    for c in range(col_count):
        highest_from_left = update_is_visible(rows, r, c, highest_from_left)
        highest_from_right = update_is_visible(rows, r, col_count-c-1, highest_from_right)
for c in range(col_count):
    highest_from_up, highest_from_down = -1, -1
    for r in range(row_count):
        highest_from_up = update_is_visible(rows, r, c, highest_from_up)
        highest_from_down = update_is_visible(rows, row_count-r-1, c, highest_from_down)
visible_map = [[tree['visible'] for tree in row] for row in rows]
visible = 0
for tree_row in visible_map:
    visible += tree_row.count(1)
print(visible)
scenic_scores = [[] for line in lines]
for r in range(len(lines)):
    scenic_scores[r] = [calc_scenic_score(rows, r, c) for c in range(len(lines[0]))]
max_row_scores = max([max(scenic_row) for scenic_row in scenic_scores])
print(max_row_scores)


SNAU_POW_LOOKUP = [5**p for p in range(22)]
SNAU_DICT = {'2':2, '1':1, '0':0, '-':-1, '=':-2}

def snau_to_int(snau):
    return sum([SNAU_DICT[snau[-1-i]]*SNAU_POW_LOOKUP[i] for i in range(len(snau))])

def int_to_snau(value):
    i = 0
    found = False
    snau = []
    while not found:
        max_snau = ['2' for k in range(i+1)]
        min_snau = ['=' for k in range(i+1)]
        min_snau[0] = '1'
        if snau_to_int(min_snau) <= value and value <= snau_to_int(max_snau):
            found = True
        else:
            i += 1
    for i in range(0, len(max_snau)):
        digits = ['2', '1', '0', '-', '=']
        digit_found = False
        for d in digits:
            if not digit_found:
                max_snau[i] = d
                min_snau[i] = d
                if snau_to_int(min_snau) <= value and value <= snau_to_int(max_snau):
                    digit_found = True
    return ''.join(max_snau)


with open('25i.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines()]
values = [snau_to_int(l) for l in lines]
print(int_to_snau(sum(values)))

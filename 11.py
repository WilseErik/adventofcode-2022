part_2 = True

class Item:
    def __init__(self, value):
        self.start_value = value
        self.value = value
        self.remainders = {}

    def add_divisor(self, divisor):
        self.remainders[divisor] = self.start_value % divisor

    def add(self, term):
        if part_2:
            for divisor in self.remainders:
                self.remainders[divisor] = (self.remainders[divisor]+term)%divisor
        else:
            self.value += term

    def multiply(self, factor):
        if part_2:
            for divisor in self.remainders:
                self.remainders[divisor] = (self.remainders[divisor]*factor)%divisor
        else:
            self.value *= factor

    def square(self):
        if part_2:
            for divisor in self.remainders:
                self.remainders[divisor] = (self.remainders[divisor]*self.remainders[divisor])%divisor
        else:
            self.value *= self.value

    def is_divisible_by(self, divisor):
        if part_2:
            return (0 == self.remainders[divisor])
        else:
            return (0 == self.value % divisor)

class Monkey:
    def __init__(self, def_lines):
        self.id = int(def_lines[0][len('Monkey '):-1])
        self.items = [Item(int(item)) for item in def_lines[1][def_lines[1].find(':')+2:].split(', ')]
        self.operation = def_lines[2][def_lines[2].find('old')+4]
        self.operation_arg = def_lines[2][def_lines[2].find(self.operation)+2:]
        self.divisor = int(def_lines[3][def_lines[3].find('divisible by ')+len('divisible by '):])
        self.next_if_true = int(def_lines[4][def_lines[4].find('throw to monkey ')+len('throw to monkey '):])
        self.next_if_false = int(def_lines[5][def_lines[5].find('throw to monkey ')+len('throw to monkey '):])
        self.next = [0 for i in range(len(self.items))]
        self.items_handled = 0
        
    def update_items(self, part_2):
        for i in range(len(self.items)):
            if 'old' in self.operation_arg:
                self.items[i].square()
            else:
                arg = int(self.operation_arg)
                if '+' in self.operation:
                    self.items[i].add(arg)
                else:
                    self.items[i].multiply(arg)
            if not part_2:
                self.items[i].value = int(self.items[i].value/int(3)) 
            self.items_handled += 1
            if self.items[i].is_divisible_by(self.divisor):
                self.next[i] = self.next_if_true
            else:
                self.next[i] = self.next_if_false

    def throw_away_items(self):
        self.items = []
        self.next = []

    def catch_item(self, new_item):
        self.items.append(new_item)
        self.next.append(0)

with open('11ia.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
monkey_lines = []
monkies = []
for line in lines:
    if len(line.strip()) > 0:
        monkey_lines.append(line)
    if 'If false:' in line:
        monkies.append(Monkey(monkey_lines))
        monkey_lines = []

monkey_divisors = []
for monkey in monkies:
    monkey_divisors.append(monkey.divisor)
for monkey in monkies:
    for divisor in monkey_divisors:
        for item in monkey.items:
            item.add_divisor(divisor)

rounds_count = 20

if part_2:
    rounds_count = 10000

for n_round in range(rounds_count):
    for monkey in monkies:
        monkey.update_items(part_2)
        for i in range(len(monkey.items)):
            monkies[monkey.next[i]].catch_item(monkey.items[i])
        monkey.throw_away_items()

inspections = [monk.items_handled for monk in monkies]
inspections.sort()
print(inspections)
print(inspections[-1]*inspections[-2])

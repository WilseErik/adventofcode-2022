import time

class Node:
	def __init__(self, line):
		fields = line.split(' ')
		self.name = fields[0][0:4]
		self.is_value = len(fields) == 2
		self.varies_with_humn = False
		if self.is_value:
			self.value = int(fields[1])
		else:
			self.arg1_name = fields[1]
			self.operation = fields[2]
			self.arg2_name = fields[3]
			self.arg1 = None
			self.arg2 = None

	def __repr__(self):
		if self.is_value:
			return '{}: {}'.format(self.name, self.value)
		else:
			return '{}: {} {} {} {}'.format(self.name, self.arg1_name, self.operation, self.arg2_name, self.varies_with_humn)

	def evaluate(self):
		return_value = 0
		if self.is_value:
			return_value = self.value
		else:
			if '+' == self.operation:
				return_value = self.arg1.evaluate() + self.arg2.evaluate()
			elif '-' == self.operation:
				return_value = self.arg1.evaluate() - self.arg2.evaluate()
			elif '*' == self.operation:
				return_value = self.arg1.evaluate() * self.arg2.evaluate()
			elif '/' == self.operation:
				return_value = self.arg1.evaluate() / self.arg2.evaluate()
		self.last_value = return_value
		return return_value

	def set_depends_on_humn(self):
		if self.is_value:
			if self.name == 'humn':
				self.varies_with_humn = True
			else:
				self.varies_with_humn = False
		else:
			if self.arg1.set_depends_on_humn():
				self.varies_with_humn = True
			if self.arg2.set_depends_on_humn():
				self.varies_with_humn = True
		return self.varies_with_humn

	def reevaluate(self):
		if not self.varies_with_humn:
			return self.last_value
		else:
			return self.evaluate()


with open('21i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
nodes = [Node(l) for l in lines]

root_node = None
humn_node = None
for n in nodes:
	if 'root' == n.name:
		root_node = n
	if 'humn' == n.name:
		humn_node = n
	if not n.is_value:
		for k in nodes:
			if n.arg1_name in k.name:
				n.arg1 = k
			if n.arg2_name in k.name:
				n.arg2 = k

start_time = time.time()

# Part 1
root_node.set_depends_on_humn()
print('Part 1: {}'.format(root_node.evaluate()))

# Part 2
left_node = root_node.arg1
right_node = root_node.arg2
root_node.evaluate()



def func(x):
	humn_node.value = x
	return left_node.reevaluate() - right_node.reevaluate()

x = 3500
step_length = 0.01
error = func(x)
while error > 1e-6:
	error = func(x)
	deriv = func(x)-func(x+1)
	print((deriv, error, x))
	x -= error*(func(x+1)-func(x))*step_length
print('Part 2: {}'.format(x))
print("--- %s seconds ---" % (time.time() - start_time))
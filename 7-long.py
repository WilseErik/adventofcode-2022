class Node:
    def __init__(self, name, parent, size=0, file=True, level=0):
        self.name = name
        self.children = []
        self.parent = parent
        self.size = size
        self.is_file = file
        self.level = level

    def add_child(self, name, size=0, file=True):
        child = self.get_child(name)
        if child is None:
            child = Node(name, self, size, file, level=self.level+1)
            self.children.append(child)
        return child

    def get_child(self, name):
        child = None
        for c in self.children:
            if c.name == name:
                child = c
        return child

    def calculate_size(self):
        if not self.is_file:
            self.size = sum([child.calculate_size() for child in self.children])
        return self.size

    def count_size_of_directories_smaller_than(self, size_limit):
        if self.is_file:
            return 0
        if self.size <= size_limit:
            return self.size + sum(child.count_size_of_directories_smaller_than(size_limit) for child in self.children)
        else:
            return sum(child.count_size_of_directories_smaller_than(size_limit) for child in self.children)

    def print(self):
        indentaion = ''.join('  ' for i in range(self.level))
        if self.is_file:
            print('{:}-{:} (file, size={:})'.format(indentaion, self.name, self.size))
        else:
            print('{:}-{:} (dir, size={:})'.format(indentaion, self.name, self.size))
        for c in self.children:
            c.print()

    def get_dir_sizes(self):
        if self.is_file:
            return []
        sizes = [self.size]
        for c in self.children:
            sizes = sizes + c.get_dir_sizes()
        return sizes


with open('7i.txt', 'r') as f:
    lines = f.readlines()
root = Node('root', None, file=False)
current_node = root
for line in lines:
    line = line.strip()
    if '$ cd ' in line:
        dir_name = line[line.find('$ cd ')+len('$ cd '):]
        if '..' == dir_name:
            current_node = current_node.parent
        else:
            current_node = current_node.add_child(dir_name, file=False)
    elif '$ ls' in line:
        pass
    elif line[0:len('dir ')] == 'dir ':
        current_node.add_child(line[len('dir '):], size=0, file=False)
    else:
        fields = line.split()
        current_node.add_child(fields[1], size=int(fields[0]), file=True)
print(root.calculate_size())
print(root.count_size_of_directories_smaller_than(100000))
print(min([x for x in root.get_dir_sizes() if x >= (30000000 - (70000000 - root.size))]))
#root.print()



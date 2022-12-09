class Node:
    def __init__(self, name, parent, size=0, file=True):
        self.name = name
        self.children = []
        self.parent = parent
        self.size = size
        self.is_file = file

    def add_child(self, name, size=0, file=True):
        self.children.append(Node(name, self, size, file))
        return self.children[-1]

    def calculate_size(self):
        if not self.is_file:
            self.size = sum([child.calculate_size() for child in self.children])
        return self.size

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
print(sum([x for x in root.get_dir_sizes() if x < 100000]))
print(min([x for x in root.get_dir_sizes() if x >= (30000000 - (70000000 - root.size))]))

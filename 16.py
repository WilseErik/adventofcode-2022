import time

class Valve:
    def __init__(self, name, flow_rate, edge_names):
        self.name = name
        self.flow_rate = flow_rate
        self.edges = []
        self.edge_names = edge_names
        self.y = 0

    def __lt__(self, other):
         return self.y < other.y

    def __repr__(self):
        #edge_str = ['{}:{}'.format(e['e'].name, e['t']) for e in self.edges]
        #return 'Name: {:}, Flow: {:}, Edges: {:}'.format(self.name, self.flow_rate, str(edge_str))
        return self.name

with open('16i.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]
valves = []
for line in lines:
    name = line[len('Valve '):len('Valve AA')]
    flow = int(line[line.find('=')+1:line.find(';')])
    edges_str = line[line.find('to valve')+len('to valve'): ]
    if edges_str[0] == 's':
        edges_str = edges_str[2:]
    else:
        edges_str = edges_str[1:]
    edges = edges_str.split(', ')
    valves.append(Valve(name, flow, edges))
for v in valves:
    for node in valves:
        if node.name in v.edge_names:
            v.edges.append({'e':node, 't':1})
    if v.name == 'AA':
        start_node = v

#
# Remove nodes with flow 0
#
done = False
while not done:
    done = True
    for node in valves:
        if node.flow_rate == 0 and done:
            if len(node.edges) == 2:
                a = node.edges[0]
                b = node.edges[1]
                travel_time = a['t'] + b['t']
                for e in a['e'].edges:
                    if e['e'] == node:
                        e['e'] = b['e']
                        e['t'] = travel_time
                for e in b['e'].edges:
                    if e['e'] == node:
                        e['e'] = a['e']
                        e['t'] = travel_time
                valves.remove(node)
                done = False

max_flow_rate = sum([node.flow_rate for node in valves])
global_max_score = 0
global_opened = []


def calc_min_distance_between_nodes(nodes, source, destination):
    # Run Dijkstra's algorithm
    unchecked_nodes = [node for node in nodes]
    for node in unchecked_nodes:
        node.y = 2**15
    source.y = 0
    current_node = source
    while len(unchecked_nodes) > 0:
        unchecked_nodes.sort()
        current_node = unchecked_nodes[0]
        unchecked_nodes.remove(current_node)
        for edge in current_node.edges:
            if current_node.y + edge['t'] < edge['e'].y:
                edge['e'].y = current_node.y + edge['t']
    return destination.y


def search_paths_in_complete_graph(node, opened_valves, time, score, flow):
    global global_max_score
    return_score = -1
    unopened_found = False
    TIME_LIMIT = 30-0
    if score + (30-time)*max_flow_rate < global_max_score:
        return -1
    for e in node.edges:
        if e['e'] not in opened_valves:
            unopened_found = True
            if time+e['t'] < TIME_LIMIT:
                new_opened_valves = opened_valves.copy()
                new_opened_valves.append(e['e'])
                new_flow = flow+e['e'].flow_rate
                new_score = search_paths_in_complete_graph(e['e'], 
                    new_opened_valves,
                    time+e['t'],
                    score+(e['t'])*flow,
                    new_flow)
                if new_score > return_score:
                    return_score = new_score
            else:
                new_score = score + flow*(TIME_LIMIT-time)
                if new_score > return_score:
                    return_score = new_score
    if not unopened_found:
        return_score = score + flow*(TIME_LIMIT-time)
    if return_score > global_max_score:
        global_max_score = return_score
    return return_score


#
# Transpose the graph to a complete graph 
#
start_time = time.time()
dist_matrix = []
complete_graph = [Valve(valves[k].name, valves[k].flow_rate, []) for k in range(len(valves))]
for k in range(len(valves)):
    dist_from_node = []
    for i in range(len(valves)):
        dist_from_node.append(calc_min_distance_between_nodes(valves, valves[k], valves[i]))
        dist_matrix.append(dist_from_node)
        if i != k:
            complete_graph[k].edge_names.append(valves[i].name)
            complete_graph[k].edges.append({'e':complete_graph[i], 't':dist_from_node[-1]+1})
global_max_score = 0

for n in range(len(complete_graph)):
    if complete_graph[n].name == 'AA':
        start_node = complete_graph[n]
        complete_graph[n] = complete_graph[0]
        complete_graph[0] = start_node



# ==============================================================================
# Part 1
# ==============================================================================

print('....................')
a = search_paths_in_complete_graph(start_node, [start_node], 4, 0, 0)
print(a)    
print("--- %s seconds ---" % (time.time() - start_time))


# ==============================================================================
# Part 2
# ==============================================================================

best_score = -1
i_len = 2**(len(complete_graph)-1)
for i in range(i_len):
    if 0 == i % 100:
        print('Progress: {:} %, best: {:}'.format(i/i_len*100, best_score))
    part_a_opened = [start_node]
    part_b_opened = [start_node]
    for n in range(len(complete_graph)-1):
        if (1 << (n+1)) & (i << 1):
            part_a_opened.append(complete_graph[n+1])
        else:
            part_b_opened.append(complete_graph[n+1])
    global_max_score =-1
    a = search_paths_in_complete_graph(start_node, part_a_opened, 4, 0, 0)
    global_max_score =-1
    b = search_paths_in_complete_graph(start_node, part_b_opened, 4, 0, 0)
    best = a+b
    if best > best_score:
        best_score = best
print('>>>>>>>>>>>>>>>>>')        
print(best_score)

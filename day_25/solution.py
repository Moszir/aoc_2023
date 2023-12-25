import random

import networkx

USE_REAL_INPUT = 1

file_path = 'input.txt' if USE_REAL_INPUT != 0 else 'example.txt'
graph = networkx.Graph()
nodes = []
with open(file_path) as f:
    for line in f.readlines():
        v = line.split(': ')[0]
        nodes.append(v)
        for w in line.split(': ')[1].strip().split(' '):
            print(v, w)
            graph.add_edge(v, w, capacity=1)

cut_value = 0
while cut_value != 3:
    v = random.choice(nodes)
    w = random.choice(nodes)
    cut_value, partition = networkx.minimum_cut(graph, v, w)
    print(cut_value)
    print(partition)
    print(len(partition[0]) * len(partition[1]))

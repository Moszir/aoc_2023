import itertools
import typing

import networkx

type Node = typing.Tuple[int, int]


file_path = 'input_2.txt'
with open(file_path) as f:
    lines = f.read().strip().split('\n')

R = len(lines)
C = len(lines[0])


def neighbors(r_, c_) -> typing.Iterator[Node]:
    for nr_, nc_ in ((r_ - 1, c_), (r_ + 1, c_), (r_, c_ - 1), (r_, c_ + 1)):
        if 0 <= nr_ < R and 0 <= nc_ < C and lines[nr_][nc_] == '.':
            yield nr_, nc_


start = (0, 1)
target = (140, 139)
junctions = [
    (r, c)
    for r, c in itertools.product(range(R), range(C))
    if lines[r][c] == '.' and 2 < sum((1 for _ in neighbors(r, c)))
]
junctions.extend((start, target))


graph = networkx.Graph()
for node1, node2 in itertools.combinations(junctions, 2):
    visited = set()
    d = [[0 for c in range(C)] for r in range(R)]
    q = [node1]
    dist = None
    while q:
        r, c = q.pop(0)
        if (r, c) in visited:
            continue
        visited.add((r, c))
        for nr, nc in neighbors(r, c):
            if (nr, nc) == node2:
                dist = d[r][c]+1
                q = []
                break
            if (nr, nc) not in visited and (nr, nc) not in junctions:
                d[nr][nc] = d[r][c]+1
                q.append((nr, nc))
    if dist is not None:
        graph.add_edge(node1, node2, weight=dist)

print(graph)

count = 0
max_length = 0
for path in networkx.all_simple_paths(graph, start, target):
    count += 1
    if count % 10_000 == 0:
        print(count, max_length)
    path_weight = networkx.path_weight(graph, path, 'weight')
    if path_weight > max_length:
        max_length = path_weight
        print('New max', max_length)

print('Finished', count, max_length)

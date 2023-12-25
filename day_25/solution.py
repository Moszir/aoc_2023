import itertools
import networkx


for real_input in (0, 1):
    file_path = 'input.txt' if real_input != 0 else 'example.txt'
    expected_solution = (514_786 if real_input != 0 else 54)

    graph = networkx.Graph()
    nodes = []
    with open(file_path) as f:
        for line in f.readlines():
            v = line.split(': ')[0]
            nodes.append(v)
            for w in line.split(': ')[1].strip().split(' '):
                graph.add_edge(v, w, capacity=1)

    for v, w in itertools.combinations(nodes, 2):
        cut_value, partition = networkx.minimum_cut(graph, v, w)
        if cut_value == 3:
            solution = len(partition[0]) * len(partition[1])
            print(solution)
            assert solution == expected_solution
            break

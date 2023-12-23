import copy
from collections import defaultdict, deque
import math


# file_path = 'example.txt'
file_path = 'input.txt'
with open(file_path) as f:
    lines = f.read().strip().split('\n')
    lines = [[c for c in line] for line in lines]

R = len(lines)
C = len(lines[0])

for r in range(R):
    for c in range(C):
        if lines[r][c] in ('v', '^', '<', '>'):
            lines[r][c] = '.'
original_lines = copy.deepcopy(lines)

start = (0, 1)
target = (140, 139)
assert lines[target[0]][target[1]] == '.'

multi_choices = set()

def get_possible_next_moves(r, c):
    return (
        [(r+1, c)] if lines[r][c] == 'v' else
        [(r-1, c)] if lines[r][c] == '^' else
        [(r, c-1)] if lines[r][c] == '<' else
        [(r, c+1)] if lines[r][c] == '>' else
        [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    )

def find_a_path():
    global multi_choices
    D = [[0 for _ in range(C)] for i in range(R)]
    q = [start]
    visited = set()
    while q:
        r, c = q.pop(-1)
        if (r, c) in visited:
            continue
        visited.add((r, c))
        choices = []
        for nr, nc in get_possible_next_moves(r, c):
            if nr < 0 or nr >= R or nc < 0 or nc >= C or lines[nr][nc] == '#' or (nr, nc) in visited:
                continue
            choices.append((nr, nc))
            # if (nr, nc) in visited:
            #     continue
            D[nr][nc] = D[r][c] + 1
            q.append((nr, nc))
        if len(choices) > 1 and len(multi_choices) == 0:
            multi_choices = set(choices)
    if D[target[0]][target[1]] != 0:
        return D[target[0]][target[1]]
    else:
        return None


max_value = 0
v = find_a_path()
if v is not None and v > max_value:
    max_value = v

closing = []
for r, c in multi_choices:
    t = (r, c)
    s = set()
    s.add(t)
    closing.append(s)

already_processeding = copy.deepcopy(closing)

while closing:
    print(len(closing))
    clo = closing.pop()
    lines = copy.deepcopy(original_lines)
    for r, c in clo:
        lines[r][c] = '#'
        # print('Closing', r, c)
    multi_choices = []
    v = find_a_path()
    # print(v)
    if v is not None:
        if v > max_value:
            max_value = v
        print('v', max_value)
        for r, c in multi_choices:
            clo2 = copy.deepcopy(clo)
            clo2.add((r, c))
            if clo2 not in already_processeding:
                closing.append(clo2)
                already_processeding.append(clo2)


# 5706 too small
# 6290 7:29:30  +10m

from collections import defaultdict, deque
import math


# file_path = 'example.txt'
file_path = 'input.txt'
with open(file_path) as f:
    lines = f.read().strip().split('\n')

# print(lines)
R = len(lines)
C = len(lines[0])
print(R, C)

r0, c0 = (0, 0)
found = False
for r in range(R):
    for c in range(C):
        if lines[r][c] == 'S':
            found = True
            r0, c0 = r, c
            break
    if found:
        break

assert found
# print(r, c)

# dijkstra = [[None for _ in line] for line in lines]
# dijkstra[r][c] = 0
# print(dijkstra)

steps = 26_501_365
q = {(r0, c0)}
values = []
i = 0
while True:
    i += 1
    # p = q.pop(0)
    next_q = set()
    for r, c in q:
        for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
            if lines[nr % R][nc % C] != '#':
                next_q.add((nr, nc))
            # if dijkstra[nr][nc] is None or dijkstra[r][c] + 1 < dijkstra[nr][nc]:
            #     dijkstra[nr][nc] = dijkstra[r][c] + 1
            #     q.append((nr, nc))
    q = next_q
    if i % R == steps % R:
        values.append(len(q))
        if len(values) == 3:
            break



# a0, a1 = values
a0, a1, a2 = values
k = steps // R
k_choose_2 = (k*(k-1)) // 2

# sol = a0 + k * (a1-a0
sol = a0 + k * (a1-a0) + k_choose_2 * ((a2-a1)-(a1-a0))

print(sol)


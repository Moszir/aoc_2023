from collections import defaultdict, deque
import math


# file_path = 'example.txt'
file_path = 'input.txt'
with open(file_path) as f:
    lines = f.read().strip().split('\n')

print(lines)
R = len(lines)
C = len(lines[0])
print(R, C)

r, c = (0, 0)
found = False
for r in range(R):
    for c in range(C):
        if lines[r][c] == 'S':
            found = True
            break
    if found:
        break

assert found
print(r, c)

dijkstra = [[None for _ in line] for line in lines]
dijkstra[r][c] = 0
print(dijkstra)

q = [(r, c)]
while q:
    p = q.pop(0)
    for nr, nc in ((p[0]+1, p[1]), (p[0]-1, p[1]), (p[0], p[1]+1), (p[0], p[1]-1)):
        if nr < 0 or nr >= R or nc < 0 or nc >= C:
            continue
        if lines[nr][nc] == '#':
            continue
        if dijkstra[nr][nc] is None or dijkstra[p[0]][p[1]] + 1 < dijkstra[nr][nc]:
            dijkstra[nr][nc] = dijkstra[p[0]][p[1]] + 1
            q.append((nr, nc))

print(dijkstra)

print(sum(
    1
    for line in dijkstra
    for k in line
    if k is not None and k % 2 == 0 and k <= 64
))


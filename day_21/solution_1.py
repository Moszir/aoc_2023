# file_path = 'example.txt'
file_path = 'input.txt'
with open(file_path) as f:
    lines = f.read().strip().split('\n')

R = len(lines)
C = len(lines[0])

r0, c0 = next((
    (r, c)
    for r in range(R)
    for c in range(C)
    if lines[r][c] == 'S'))

dijkstra = [[65 for _ in line] for line in lines]
dijkstra[r0][c0] = 0

q = [(r0, c0)]
while q:
    r, c = q.pop(0)
    for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
        if nr < 0 or nr >= R or nc < 0 or nc >= C:
            continue
        if lines[nr][nc] == '#':
            continue
        if dijkstra[r][c] + 1 < dijkstra[nr][nc]:
            dijkstra[nr][nc] = dijkstra[r][c] + 1
            q.append((nr, nc))

solution = sum(
    1
    for line in dijkstra
    for k in line
    if k % 2 == 0 and k <= 64)  # 6 for the example file

print(solution)
assert solution == 3_814

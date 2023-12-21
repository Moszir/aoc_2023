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

steps = 26_501_365
values = []
q = {(r0, c0)}

for i in range(1, 2*R + steps % R + 1):
    next_q = set()
    for r, c in q:
        for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
            if lines[nr % R][nc % C] != '#':
                next_q.add((nr, nc))
    q = next_q
    if i % R == steps % R:
        values.append(len(q))


a0, a1, a2 = values
k = steps // R
k_choose_2 = (k*(k-1)) // 2
sol = a0 + k * (a1-a0) + k_choose_2 * ((a2-a1)-(a1-a0))
print(sol)
assert sol == 632_257_949_158_206


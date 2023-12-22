from collections import defaultdict, deque
import math


# file_path = 'example.txt'
file_path = 'input.txt'
with open(file_path) as f:
    lines = f.read().strip().split('\n')

bricks = []
for line in lines:
    p = line.strip().split('~')[0]
    q = line.strip().split('~')[1]
    bricks.append([int(p.split(',')[0]), int(p.split(',')[1]), int(p.split(',')[2]), int(q.split(',')[0]), int(q.split(',')[1]), int(q.split(',')[2])])

# print(bricks)

def proj(brick):
    return [
        (x, y)
        for x in range(brick[0], brick[3]+1)
        for y in range(brick[1], brick[4]+1)]


change_happened = True
while change_happened:
    change_happened = False
    for i, brick in enumerate(bricks):
        z = brick[2]
        min_z = 1
        my_proj = proj(brick)
        for j, b2 in enumerate(bricks):
            if j == i:
                continue
            if b2[2] >= z or b2[5] < min_z:
                continue
            b2_proj = proj(b2)
            if any((p in b2_proj for p in my_proj)):
                min_z = b2[5]+1
                # print(brick, my_proj, 'is blocked by', b2, b2_proj)
        if min_z < z:
            fall = z-min_z
            brick[2] = min_z
            brick[5] -= fall
            change_happened = True
# 5

# print(bricks)

supported_by = [[] for b in bricks]

for i, b in enumerate(bricks):
    b_proj = proj(b)
    for j, b2 in enumerate(bricks):
        if i == j:
            continue
        if b2[5]+1 != b[2]:
            continue
        b2_proj = proj(b2)
        if any((p in b2_proj for p in b_proj)):
            supported_by[i].append(j)

# print(supported_by)
# eliminateable: no [i] exists
print(
    sum((
        1
        for i in range(len(bricks))
        if [i] not in supported_by)))

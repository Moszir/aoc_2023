import itertools
import typing
import math
from scipy.optimize import fsolve
# from z3 import *

# file_path = 'example.txt'
file_path = 'input.txt'
with open(file_path) as f:
    lines = f.read().strip().split('\n')
    entries = []
    for line in lines:
        fp = line.split('@')[0]
        lp = line.split('@')[1]
        entries.append([
            int(fp.split(',')[0]), int(fp.split(',')[1]), int(fp.split(',')[2]),
            int(lp.split(',')[0]), int(lp.split(',')[1]), int(lp.split(',')[2])
        ])

# print(entries)


def intersect_xy(line1: typing.List[int], line2: typing.List[int]):
    A_ = [line1[3], -line2[3], line1[4], -line2[4]]
    b_ = [line2[0] - line1[0], line2[1] - line1[1]]
    if A_[0] == 0:
        if A_[2] == 0:
            return None
        assert A_[1] != 0
        t2 = b_[0] / A_[1]
        t1 = (b_[1] - A_[3] * t2) / A_[0]  # todo opt
        return (line2[0] + t2 * line2[3], line2[1] + t2 * line2[4]) if t2 > 0 and t1 > 0 else None
    else:
        A_[3] -= (A_[2] / A_[0]) * A_[1]
        b_[1] -= (A_[2] / A_[0]) * b_[0]
        A_[2] = 0
        if A_[3] == 0:
            return None
        t2 = b_[1] / A_[3]
        t1 = (b_[0] - A_[1] * t2) / A_[0]  # opt
        return (line2[0] + t2 * line2[3], line2[1] + t2 * line2[4]) if t2 > 0 and t1 > 0 else None
    # solve x1 + t1*v1x = x2 + t2*v2x
    #       y1 + t1*v1y = y2 + t2*v2y
    # v1x -v2x | x2 - x1
    # v1y -v2y | y2 - y1


accu = 0
for a, b in itertools.combinations(entries, 2):
    inti = intersect_xy(a, b)
    # if inti is not None and 7 <= inti[0] <= 27 and 7 <= inti[1] <= 27:
    if inti is not None and 200000000000000 <= inti[0] <= 400000000000000 and 200000000000000 <= inti[1] <= 400000000000000:
        accu += 1
    # print(a, b, intersect_xy(a, b))

print(accu)


# part 2

# Find xr, yr, zr, vxr, vyr, vzr such that
# xr + T * vxr = x0 + T vx0
# yr + T * vyr = y0 + T vy0
# zr + T * vzr = z0 + T vz0
# is solvable for every xyz, v xyz

# T = (x0 - xr) / (vxr - vx0)
# T = (y0 - yr) / (vyr - vy0)
# T = (z0 - zr) / (vzr - vz0)
# for i, entry in enumerate(entries):
#     print('{}, {}, {}'.format(
#         f'x + t{i} * vx - {entry[0]} - t{i}*{entry[3]}',
#         f'y + t{i} * vy - {entry[1]} - t{i}*{entry[4]}',
#         f'z + t{i} * vz - {entry[2]} - t{i}*{entry[5]}'
#     ))


def equations(p):
    x_, y_, z_, vx_, vy_, vz_ = p
    res = []
    for i in entries[1:4]:
        x1, y1, z1, vx1, vy1, vz1 = i
        res.append((x_ - x1) * (vy_ - vy1) - (y_ - y1) * (vx_ - vx1))
        res.append((x_ - x1) * (vz_ - vz1) - (z_ - z1) * (vx_ - vx1))
    return res


x, y, z, xv, yv, zv = fsolve(equations, entries[0])

print(x)
print(y)
print(z)
print(int(round(x+y+z)))
# and add +1, because the rounding was wrong -.-








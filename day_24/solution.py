import itertools
import typing
from collections import defaultdict, deque
import math

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

import itertools
import random
import typing
from scipy.optimize import fsolve

# file_path = 'example.txt'
file_path = 'input.txt'
with open(file_path) as f:
    entries = [
        tuple(
            int(x)
            for part in line.split('@')
            for x in part.split(',')
        )
        for line in f.readlines()
    ]

HailStone = typing.Tuple[int, int, int, int, int, int]
XyPoint = typing.Tuple[float, float]


def intersect_xy(line1: HailStone, line2: HailStone) -> typing.Optional[XyPoint]:
    """ Intersect the two lines in the x-y plane.

    Solve the following system:
    x1 + t1*v1x = x2 + t2*v2x
    y1 + t1*v1y = y2 + t2*v2y

    In matrix form:
    v1x, -v2x | x2 - x1
    v1y, -v2y | y2 - y1
    """
    A_ = [line1[3], -line2[3], line1[4], -line2[4]]
    b_ = [line2[0] - line1[0], line2[1] - line1[1]]
    if A_[0] == 0:
        if A_[2] == 0:
            return None
        assert A_[1] != 0
        t2 = b_[0] / A_[1]
        t1 = (b_[1] - A_[3] * t2) / A_[0]
        return (line2[0] + t2 * line2[3], line2[1] + t2 * line2[4]) if t2 > 0 and t1 > 0 else None
    else:
        A_[3] -= (A_[2] / A_[0]) * A_[1]
        b_[1] -= (A_[2] / A_[0]) * b_[0]
        A_[2] = 0
        if A_[3] == 0:
            return None
        t2 = b_[1] / A_[3]
        t1 = (b_[0] - A_[1] * t2) / A_[0]
        return (line2[0] + t2 * line2[3], line2[1] + t2 * line2[4]) if t2 > 0 and t1 > 0 else None


target_min = 200_000_000_000_000  # 7 for the example
target_max = 400_000_000_000_000  # 27 for the example

accu = 0
for a, b in itertools.combinations(entries, 2):
    result = intersect_xy(a, b)
    if result is not None:
        accu += 1 if all((target_min <= c <= target_max for c in result)) else 0

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
#
# that is really just 2 equations for the xyz, vxyz of the rock:
#  (x0 - x) / (vx - vx0) == (y0 - y) / (vy - vy0)  -->  (x-x0)*(vy-vy0) - (y-y0)*(vx-vx0) == 0
#  (x0 - x) / (vx - vx0) == (z0 - z) / (vz - vz0)  -->  (x-x0)*(vz-vz0) - (z-z0)*(vx-vx0) == 0

# Add some Monte-Carlo voting system to combat uncertainty (thanks to D. Hanak)
id1, id2, id3 = 0, 0, 0


def randomize_ids():
    global id1, id2, id3
    id1 = random.choice(range(300))
    id2 = random.choice(range(300))
    while id2 == id1:
        id2 = random.choice(range(300))
    id3 = random.choice(range(300))
    while id3 in (id1, id2):
        id3 = random.choice(range(300))


def equations(p):
    x_, y_, z_, vx_, vy_, vz_ = p
    res = []
    # 6 equations for the 6 variables, start from entries[0]
    global id1, id2, id3
    for entry_id in (id1, id2, id3):
        x1, y1, z1, vx1, vy1, vz1 = entries[entry_id]
        res.append((x_ - x1) * (vy_ - vy1) - (y_ - y1) * (vx_ - vx1))
        res.append((x_ - x1) * (vz_ - vz1) - (z_ - z1) * (vx_ - vx1))
    return res


# For every entry as a starting point, solve 10 random equation system, and vote for the result
votes = []
for i in range(300):
    start = entries[i]
    for j in range(10):
        randomize_ids()
        x, y, z, vx, vy, vz = fsolve(equations, start, xtol=1e-16)
        v = round(x) + round(y) + round(z)
        votes.append(v)

vote_values = set(votes)
vote_counts = sorted([(sum((1 for v in votes if v == vote_value)), vote_value) for vote_value in vote_values], reverse=True)

print(vote_counts[0])
assert vote_counts[0][1] == 578_177_720_733_043

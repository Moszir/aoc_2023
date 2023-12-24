import itertools
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


def equations(p):
    x_, y_, z_, vx_, vy_, vz_ = p
    res = []
    # 6 equations for the 6 variables, start from entries[0]
    for i in entries[1:4]:
        x1, y1, z1, vx1, vy1, vz1 = i
        res.append((x_ - x1) * (vy_ - vy1) - (y_ - y1) * (vx_ - vx1))
        res.append((x_ - x1) * (vz_ - vz1) - (z_ - z1) * (vx_ - vx1))
    return res


x, y, z, vx, vy, vz = fsolve(equations, entries[0])

# This is not an exact solution of course, but there's a good chance that if you hit 3 hailstones,
# then you hit all of them, because the numbers were generated that way.
# And our solution is in floats...
print(x, y, z, vx, vy, vz)
print(x+y+z)  # 578177720733042.5
# solution for my input is 578_177_720_733_043, close enough

print(round(x) + round(y) + round(z))  # This would have been better, matching the actual solution

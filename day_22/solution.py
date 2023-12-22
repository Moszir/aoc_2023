# import cProfile
# import io
# import pstats
# from pstats import SortKey
#
# profiler = cProfile.Profile()
# profiler.enable()

real_input = True
file_path = 'input.txt' if real_input else 'example.txt'
expected_solution_1 = 446 if real_input else 5
expected_solution_2 = 60287 if real_input else 7

bricks = [
    [
        int(x)
        for part in line.split('~')
        for x in part.split(',')
    ]
    for line in open(file_path).readlines()
]

# This way the falling can go with a single for loop.
bricks = sorted(bricks, key=lambda b: b[2])
n = len(bricks)

xy_projections = [
    {
        (x, y)
        for x in range(brick[0], brick[3]+1)
        for y in range(brick[1], brick[4]+1)
    }
    for brick in bricks
]


for i, brick in enumerate(bricks):
    min_z = 1  # Find the largest z, that intersects with the projection of the brick
    for j in range(i):
        if bricks[j][5] >= min_z and not xy_projections[i].isdisjoint(xy_projections[j]):
            min_z = bricks[j][5]+1
    brick[5] -= brick[2]-min_z
    brick[2] = min_z

supported_by = [set() for b in bricks]

for i in range(n):
    # The bricks are no longer necessarily sorted by z, but a supporter could not have fallen below what it supports.
    for j in range(i):
        if bricks[j][5]+1 == bricks[i][2] and not xy_projections[i].isdisjoint(xy_projections[j]):
            supported_by[i].add(j)

# Brick `i` cannot be eliminated, if there is a brick that is only supported by `i`.
solution_1 = sum((1 for i in range(len(bricks)) if {i} not in supported_by))
print(solution_1)
if solution_1 != expected_solution_1:
    print("This doesn't seem right: expected", expected_solution_1, "got", solution_1)

# -------------------------------------------------------------------------------------------------
# Part 2

# assert all((all((i > j for j in s)) for i, s in enumerate(supported_by)))
# Make those on the ground be supported by '-1'
for s in supported_by:
    if not s:
        s.add(-1)

solution_2 = 0
for i in range(n):
    removed = {i}
    for j in range(i+1, n):
        if supported_by[j].issubset(removed):
            removed.add(j)
    solution_2 += len(removed) - 1  # -1: brick `i` itself

print(solution_2)
if solution_2 != expected_solution_2:
    print("This doesn't seem right: expected", expected_solution_2, "got", solution_2)

# profiler.disable()
# s = io.StringIO()
# sortby = SortKey.CUMULATIVE
# ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
# ps.print_stats()
# print(s.getvalue())

import dataclasses
import math
import unittest


def count_brute_force(time: int, record: int) -> int:
    # The brute force way, that sadly works for the second star too (~6s runtime):
    # If we hold the button for `t`, then the distance is `t*(time-t)`.
    def wins(t: int) -> bool:
        return t*(time-t) > record
    return sum((1 for t in range(time) if wins(t)))


def count_solve_quadratic(time: int, record: int) -> int:
    # If we hold the button for `t`, then the distance is `f(t) = t*(time-t)`
    # Solve the quadratic t*(time-t) == record
    # 0 = t^2 - time*t + record
    d = time**2 - 4*record
    if d < 0:
        return 0
    x1 = (time - math.sqrt(d)) / 2
    x2 = (time + math.sqrt(d)) / 2

    # We can assume that `record >= 0`, therefore x1, x2 >= 0.
    # The first `t` that wins is the smallest integer that is strictly larger than x1
    x1 = math.floor(x1 + 1)
    # The last `t` that wins is the largest integer that is strictly smaller than x2
    x2 = math.ceil(x2 - 1)  # equivalent to floor if not an integer, -1 otherwise
    return x2-x1+1


def count_binary_search(time: int, record: int) -> int:
    # If we hold the button for `t`, then the distance is `f(t) = t*(time-t)`
    def wins(t: int) -> bool:
        return t*(time-t) > record

    # `f` is an "upside down parabola", its maximum is at its middle
    # If that doesn't win, then nothing does:
    half_time = time // 2
    if not wins(half_time):
        return 0

    # To find the first `t` that wins in the [0, half_time] interval, use binary search
    @dataclasses.dataclass
    class Interval:
        no_win: int
        win: int

    s = Interval(0, half_time)  # 0 does not win, half_time does
    while s.no_win+1 != s.win:
        mid_point = (s.no_win + s.win) // 2
        if wins(mid_point):
            s.win = mid_point
        else:
            s.no_win = mid_point

    # We are symmetric in the [0, time] interval, so `time-win` is the last winning `t`.
    return (time - s.win) - s.win + 1


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]
            self.__times = [int(x) for x in lines[0].split(': ')[1].split(' ') if x != '']
            self.__records = [int(x) for x in lines[1].split(': ')[1].split(' ') if x != '']

    def solve_a(self, method=count_brute_force) -> int:
        return math.prod((
            method(time=time, record=record)
            for time, record in zip(self.__times, self.__records)
        ))

    def solve_b(self, method=count_solve_quadratic) -> int:
        time = int(''.join((str(x) for x in self.__times)))
        record = int(''.join((str(x) for x in self.__records)))
        return method(time=time, record=record)


class Tests(unittest.TestCase):
    _methods = (count_brute_force, count_solve_quadratic, count_binary_search)

    def test_a_example(self):
        for method in self._methods:
            self.assertEqual(288, Solution('example.txt').solve_a(method=method))

    def test_a_input(self):
        for method in self._methods:
            self.assertEqual(1_108_800, Solution('input.txt').solve_a(method=method))

    def test_b_example(self):
        for method in self._methods:
            self.assertEqual(71_503, Solution('example.txt').solve_b(method=method))

    def test_b_input(self):
        for method in self._methods:
            self.assertEqual(36_919_753, Solution('input.txt').solve_b(method=method))


if __name__ == '__main__':
    unittest.main()

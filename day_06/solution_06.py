import dataclasses
import typing
import unittest


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]
            self.__times = [int(x) for x in lines[0].split(': ')[1].split(' ') if x != '']
            self.__records = [int(x) for x in lines[1].split(': ')[1].split(' ') if x != '']

    @staticmethod
    def __count_ways_to_beat_record(time: int, record: int) -> int:
        # If we hold the button for `t`, then the distance is `f(t) = t*(time-t)`
        def wins(t: int) -> bool:
            return t*(time-t) > record

        # The brute force way, that sadly works for the second star too:
        # return sum((1 for t in range(time) if wins(t)))

        # Otherwise, we do some binary search
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

    def solve_a(self) -> int:
        accu = 1
        for time, record in zip(self.__times, self.__records):
            accu *= self.__count_ways_to_beat_record(time=time, record=record)
        return accu

    def solve_b(self) -> int:
        time = int(''.join((str(x) for x in self.__times)))
        record = int(''.join((str(x) for x in self.__records)))
        return self.__count_ways_to_beat_record(time=time, record=record)


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(288, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(1_108_800, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(71_503, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(36_919_753, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

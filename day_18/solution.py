import pathlib
import unittest

from moszir_utils.polygon import shoe_lace_area as area


class Solution:
    def __init__(self, path: pathlib.Path):
        self.data = path.read_text().splitlines()

    def solve_a(self) -> int:
        p = [(0, 0)]
        x, y = 0, 0
        length = 0
        for line in self.data:
            dire, dist, _ = line.split()
            dist = int(dist)
            length += dist
            x += dist if dire == 'D' else -dist if dire == 'U' else 0
            y += dist if dire == 'R' else -dist if dire == 'L' else 0
            p.append((x, y))
        # Area = Interior points + Boundary points / 2 - 1  (Pick's theorem)
        # Result = i + b = (A - b/2 + 1) + b = A + b/2 + 1
        return int(area(p)) + length // 2 + 1

    def solve_b(self) -> int:
        p = [(0, 0)]
        x, y = 0, 0
        length = 0
        for line in self.data:
            instruction = line.split()[-1][2:-1]
            dist = int(instruction[:5], 16)
            length += dist
            dire = int(instruction[5:], 16)
            dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][dire]
            x += dx * dist
            y += dy * dist
            p.append((x, y))
        return int(area(p)) + length // 2 + 1


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(62, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(95_356, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(952_408_144_115, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(92_291_468_914_147, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

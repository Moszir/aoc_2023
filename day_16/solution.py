import copy
import dataclasses
import pathlib
import typing
import unittest


class Solution:
    def __init__(self, path: pathlib.Path):
        self.lines = path.read_text().splitlines()
        self.height = len(self.lines)
        self.width = len(self.lines[0])

    @dataclasses.dataclass
    class Beam:
        row: int
        col: int
        direction: str

        def as_tuple(self):
            return self.row, self.col, self.direction

        def next(self) -> 'Solution.Beam':
            if self.direction == 'right':
                self.col += 1
            elif self.direction == 'left':
                self.col -= 1
            elif self.direction == 'down':
                self.row += 1
            elif self.direction == 'up':
                self.row -= 1
            return self

        _backslash = {
            'right': 'down',
            'down': 'right',
            'left': 'up',
            'up': 'left',
        }

        def hit_backslash(self) -> 'Solution.Beam':
            self.direction = self._backslash[self.direction]
            return self

        _slash = {
            'right': 'up',
            'up': 'right',
            'left': 'down',
            'down': 'left',
        }

        def hit_slash(self) -> 'Solution.Beam':
            self.direction = self._slash[self.direction]
            return self

        def react(self, spot: str) -> typing.List['Solution.Beam']:
            if spot == '\\':
                return [self.hit_backslash().next()]
            elif spot == '/':
                return [self.hit_slash().next()]
            elif (spot == '|' and self.direction in ('left', 'right')) or (spot == '-' and self.direction in ('up', 'down')):
                twin = copy.copy(self)
                return [self.hit_slash().next(), twin.hit_backslash().next()]
            return [self.next()]

    def count_energized_beams(self, starting_beam: Beam) -> int:
        energized = [[False for _ in line] for line in self.lines]
        beams = [starting_beam]
        seen = set()
        while len(beams) > 0:
            beam = beams.pop()
            if not (0 <= beam.row < self.height and 0 <= beam.col < self.width) or beam.as_tuple() in seen:
                continue
            seen.add(beam.as_tuple())
            energized[beam.row][beam.col] = True
            beams.extend(beam.react(self.lines[beam.row][beam.col]))
        return sum((1 for line in energized for spot in line if spot))

    def solve_a(self) -> int:
        return self.count_energized_beams(Solution.Beam(0, 0, 'right'))

    def solve_b(self) -> int:
        return max((
            self.count_energized_beams(beam)
            for beam in (
                *(Solution.Beam(0, col, 'down') for col in range(self.width)),
                *(Solution.Beam(self.height-1, col, 'up') for col in range(self.width)),
                *(Solution.Beam(row, 0, 'right') for row in range(self.width)),
                *(Solution.Beam(row, self.width-1, 'left') for row in range(self.width))
            )))


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(46, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(6_921, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(51, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(7_594, self.real_input().solve_b())  # 2.6s, good enough


if __name__ == '__main__':
    unittest.main()

import copy
import dataclasses
import itertools
import math
import pathlib
import typing
import unittest

from moszir_utils.asterisk import *


class Solution:
    def __init__(self, path: pathlib.Path):
        self.lines = path.read_text().splitlines()
        self.height = len(self.lines)
        self.width = len(self.lines[0])
        # print(self.lines)

    @dataclasses.dataclass
    class Beam:
        row: int
        col: int
        direction: str
        
        def next(self):
            if self.direction == 'right':
                self.col += 1
            if self.direction == 'left':
                self.col -= 1
            if self.direction == 'down':
                self.row += 1
            if self.direction == 'up':
                self.row -= 1

        def as_tuple(self):
            return self.row, self.col, self.direction

    def solve_a(self, starting_beam=(0, 0, 'right')) -> int:
        energized = [[0 for c in line] for line in self.lines]
        beams = [Solution.Beam(*starting_beam)]
        seen = set()
        while len(beams) > 0:
            beam = beams.pop(0)
            # print(len(beams), beam)
            if beam.as_tuple() in seen:
                continue
            seen.add(beam.as_tuple())
            if 0 <= beam.row < self.height and 0 <= beam.col < self.width:
                energized[beam.row][beam.col] += 1
                s = self.lines[beam.row][beam.col]
                if s == '.':
                    beam.next()
                    beams.append(beam)
                if s == '\\':
                    if beam.direction == 'right':
                        beam.direction = 'down'
                    elif beam.direction == 'left':
                        beam.direction = 'up'
                    elif beam.direction == 'down':
                        beam.direction = 'right'
                    elif beam.direction == 'up':
                        beam.direction = 'left'
                    beam.next()
                    beams.append(beam)
                elif s == '/':
                    if beam.direction == 'right':
                        beam.direction = 'up'
                    elif beam.direction == 'left':
                        beam.direction = 'down'
                    elif beam.direction == 'down':
                        beam.direction = 'left'
                    elif beam.direction == 'up':
                        beam.direction = 'right'
                    beam.next()
                    beams.append(beam)
                elif s == '|':
                    if beam.direction in ('up', 'down'):
                        beam.next()
                        beams.append(beam)
                    else:
                        beam2 = copy.copy(beam)
                        beam.direction = 'up'
                        beam.next()
                        beams.append(beam)
                        beam2.direction = 'down'
                        beam2.next()
                        beams.append(beam2)
                elif s == '-':
                    if beam.direction in ('left', 'right'):
                        beam.next()
                        beams.append(beam)
                    else:
                        beam2 = copy.copy(beam)
                        beam.direction = 'left'
                        beam.next()
                        beams.append(beam)
                        beam2.direction = 'right'
                        beam2.next()
                        beams.append(beam2)

        return sum((1 for line in energized for c in line if c > 0))

    def solve_b(self) -> int:
        m = 0
        for col in range(self.width):
            c = self.solve_a((0, col, 'down'))
            if c > m:
                m = c
            c = self.solve_a((self.height-1, col, 'up'))
            if c > m:
                m = c
        for row in range(self.height):
            c = self.solve_a((row, 0, 'right'))
            if c > m:
                m = c
            c = self.solve_a((row, self.width-1, 'left'))
            if c > m:
                m = c

        return m


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
        self.assertEqual(0, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

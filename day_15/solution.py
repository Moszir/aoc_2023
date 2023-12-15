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
        self.lines = path.read_text().split(',')
        # print(lines)

    def hash(self, line: str):
        accu = 0
        for c in line:
            accu += ord(c)
            accu *= 17
            accu %= 256
        return accu

    def solve_a(self) -> int:
        return sum((self.hash(line) for line in self.lines))

    def solve_b(self) -> int:
        boxes = [[] for _ in range(256)]
        for line in self.lines:
            if line[-1] == '-':
                name = line[:-1]
                box_index = self.hash(name)
                box = boxes[box_index]
                for i in range(len(box)):
                    if box[i][0] == name:
                        del box[i]
                        break
            else:
                name = line.split('=')[0]
                focal = int(line.split('=')[1])
                box_index = self.hash(name)
                box = boxes[box_index]
                found = False
                for i in range(len(box)):
                    if box[i][0] == name:
                        box[i][1] = focal
                        found = True
                        break
                if not found:
                    box.append([name, focal])
            # print(boxes)

        accu = 0
        for i, box in enumerate(boxes):
            for j, lens in enumerate(box):
                accu += (i+1) * (j+1) * lens[1]
        return accu


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(1320, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(502_139, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(145, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(284_132, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

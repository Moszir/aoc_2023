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

    def solve_a(self) -> int:
        return 0

    def solve_b(self) -> int:
        return 0


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(0, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(0, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(0, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(0, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

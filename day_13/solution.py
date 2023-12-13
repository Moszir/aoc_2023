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
        self.problems = path.read_text().split('\n\n')

    def find_horizontal(self, rows: typing.List[str]) -> typing.Optional[int]:
        for i in range(len(rows)-1):
            match = True
            for j in range(i+1):
                opposite = (2*(i+1)-(j+1))
                if 0 <= opposite < len(rows) and rows[j] != rows[(2*(i+1)-(j+1))]:
                    match = False
                    break
            if match:
                # print('found mirror ', i+1)
                return i+1
        return None

    def find_horizontal_b(self, rows: typing.List[typing.List[str]]) -> typing.List[int]:
        results = []
        for i in range(len(rows)-1):
            match = True
            for j in range(i+1):
                opposite = (2*(i+1)-(j+1))
                if 0 <= opposite < len(rows) and rows[j] != rows[(2*(i+1)-(j+1))]:
                    match = False
                    break
            if match:
                results.append(i+1)
                # print('found mirror ', i+1)
        return results

    def find_mirror(self, rows: typing.List[typing.List[str]]) -> int:
        # rows = problem.split('\n')
        # print(rows)
        r = self.find_horizontal(rows)
        if r is not None:
            # print('find_mirror ', 100*r)
            return 100*r
        return self.find_horizontal([''.join(col) for col in zip(*rows)])
        # # print([''.join(col) for col in zip(*rows)])

    def find_mirror_b(self, rows: typing.List[typing.List[str]], excluded_value) -> typing.Optional[int]:
        # rows = problem.split('\n')
        # print(rows)
        r = self.find_horizontal_b(rows)
        for i in r:
            if 100*i != excluded_value:
                return 100*i
        r = self.find_horizontal_b([col for col in zip(*rows)])
        for i in r:
            if i != excluded_value:
                return i
        return None
        # # print([''.join(col) for col in zip(*rows)])

    def solve_a(self) -> int:
        return sum((self.find_mirror(problem) for problem in self.problems))

    def solve_one_b(self, rows: typing.List[typing.List[str]]) -> int:
        original_solution = self.find_mirror(rows)
        print(original_solution)
        spots = len(rows) * len(rows[0])
        for ri in range(len(rows)):
            for ci in range(len(rows[0])):
                original = rows[ri][ci]
                rows[ri][ci] = '#' if original == '.' else '.'
                result = self.find_mirror_b(rows, original_solution)
                print(ri, ci, result)
                if result is not None and result != original_solution:
                    # print(ri, ci)
                    return result
                rows[ri][ci] = original
        print(rows)
        assert False
        return -1

    def solve_b(self) -> int:
        accu = 0
        i = 0
        for problem in self.problems:
            print('starting ', i)
            i += 1
            accu += self.solve_one_b(
                [[c for c in row] for row in problem.split('\n')])

        return accu


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(405, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(43614, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(400, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(0, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

import dataclasses
import typing
import unittest


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]
            self.sequences = [[int(x) for x in line.split(' ')] for line in lines]

    @staticmethod
    def extrapolate(sequence):
        table = [sequence]
        while any(x != 0 for x in table[-1]):
            table.append([])
            for i in range(len(table[-2])-1):
                table[-1].append(table[-2][i+1] - table[-2][i])
        table[-1].append(0)
        i = len(table) - 2
        while i >= 0:
            table[i].append(table[i][-1] + table[i+1][-1])
            i -= 1
        return table[0][-1]

    @staticmethod
    def extrapolate_back(sequence):
        table = [sequence]
        while any(x != 0 for x in table[-1]):
            table.append([])
            for i in range(len(table[-2])-1):
                table[-1].append(table[-2][i+1] - table[-2][i])
        solution = 0
        i = len(table) - 2
        while i >= 0:
            solution = table[i][0] - solution
            i -= 1
        return solution

    def solve_a(self) -> int:
        return sum((self.extrapolate(sequence) for sequence in self.sequences))

    def solve_b(self) -> int:
        return sum((self.extrapolate_back(sequence) for sequence in self.sequences))


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(114, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(1789635132, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(2, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(913, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

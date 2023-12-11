import dataclasses
import typing
import unittest


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            self.map = lines = [line.strip() for line in test_input.readlines()]
            self.height = len(self.map)
            self.width = len(self.map[0])
            assert all((len(line) == self.width for line in self.map))
            self.empty_lines = [
                row_idx
                for row_idx in range(len(self.map))
                if '#' not in self.map[row_idx]]
            self.empty_columns = [
                col_idx
                for col_idx in range(len(self.map[0]))
                if all((line[col_idx] == '.' for line in self.map))]
            self.galaxies = [
                (row_idx, col_idx)
                for row_idx in range(self.height)
                for col_idx in range(self.width)
                if self.map[row_idx][col_idx] == '#'
            ]
            # print(vars(self))

    def solve_a(self) -> int:
        accu = 0
        ng = len(self.galaxies)
        for i1 in range(ng):
            g1 = self.galaxies[i1]
            for i2 in range(i1+1, ng):
                g2 = self.galaxies[i2]
                lr, sr = max(g1[0], g2[0]), min(g1[0], g2[0])
                lc, sc = max(g1[1], g2[1]), min(g1[1], g2[1])
                rd = lr - sr + sum((1 for row in self.empty_lines if sr < row < lr))
                cd = lc - sc + sum((1 for col in self.empty_columns if sc < col < lc))
                accu += rd + cd

        return accu

    def solve_b(self) -> int:
        accu = 0
        ng = len(self.galaxies)
        for i1 in range(ng):
            g1 = self.galaxies[i1]
            for i2 in range(i1+1, ng):
                g2 = self.galaxies[i2]
                lr, sr = max(g1[0], g2[0]), min(g1[0], g2[0])
                lc, sc = max(g1[1], g2[1]), min(g1[1], g2[1])
                rd = lr - sr + 999999 * sum((1 for row in self.empty_lines if sr < row < lr))
                cd = lc - sc + 999999 * sum((1 for col in self.empty_columns if sc < col < lc))
                accu += rd + cd

        return accu


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(374, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(10494813, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(82000210, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(840988812853, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

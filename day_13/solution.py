import pathlib
import typing
import unittest

type Problem = typing.List[typing.List[str]]
type MaybeInt = typing.Optional[int]


class Solution:
    def __init__(self, path: pathlib.Path):
        self.problems = [
            [[c for c in row] for row in problem.split('\n')]
            for problem in path.read_text().split('\n\n')]

    @staticmethod
    def find_horizontal(rows: Problem, excluded: MaybeInt = None) -> MaybeInt:
        for i in range(len(rows)-1):
            match = True
            for j in range(i+1):
                opposite = (2*(i+1)-(j+1))
                if 0 <= opposite < len(rows) and rows[j] != rows[opposite]:
                    match = False
                    break
            if match and i+1 != excluded:
                return i+1
        return None

    def find_mirror(self, rows: Problem, excluded: MaybeInt = None) -> MaybeInt:
        excluded_row = excluded // 100 if excluded is not None and excluded % 100 == 0 else None
        r = self.find_horizontal(rows, excluded=excluded_row)
        if r is not None:
            return r*100
        return self.find_horizontal([col for col in zip(*rows)], excluded=excluded)

    def solve_a(self) -> int:
        return sum((self.find_mirror(problem) for problem in self.problems))

    def solve_one_b(self, rows: Problem) -> int:
        """ Just brute force it. """
        original_solution = self.find_mirror(rows)
        for ri in range(len(rows)):
            for ci in range(len(rows[0])):
                original = rows[ri][ci]
                rows[ri][ci] = '#' if original == '.' else '.'
                result = self.find_mirror(rows, excluded=original_solution)
                if result is not None:
                    return result
                rows[ri][ci] = original
        assert False

    def solve_b(self) -> int:
        return sum((self.solve_one_b(problem) for problem in self.problems))


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
        self.assertEqual(43_614, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(400, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(36_771, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

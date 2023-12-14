import pathlib
import unittest


class Solution:
    def __init__(self, path: pathlib.Path):
        self.lines = [[c for c in line] for line in path.read_text().splitlines()]
        self.height = len(self.lines)
        self.width = len(self.lines[0])
        # print(self.lines)

    def up(self):
        for col in range(self.width):
            for row in range(self.height):
                c = self.lines[row][col]
                if c == 'O':
                    r = row
                    while r-1 >= 0 and self.lines[r-1][col] == '.':
                        self.lines[r-1][col] = 'O'
                        self.lines[r][col] = '.'
                        r -= 1

    def score(self):
        score = 0
        for col in range(self.width):
            for row in range(self.height):
                c = self.lines[row][col]
                if c == 'O':
                    score += self.height-row
        return score

    def solve_a(self) -> int:
        self.up()
        return self.score()

    def rotate(self):
        self.lines = [list(reversed(line)) for line in zip(*self.lines)]

    def cycle(self):
        for _ in range(4):
            self.up()
            self.rotate()

    def as_string(self):
        return ''.join(''.join(line) for line in self.lines)

    def solve_b(self, cycles: int = 1_000_000_000) -> int:
        scores = []
        jumped = False
        k = 0
        while k < cycles:
            self.cycle()
            if not jumped:
                s = self.as_string()
                if s not in scores:
                    scores.append(s)
                else:
                    cycle = k - scores.index(s)
                    k += ((cycles - k) // cycle) * cycle
                    jumped = True
            k += 1
        return self.score()


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(136, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(109_661, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(64, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(90_176, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

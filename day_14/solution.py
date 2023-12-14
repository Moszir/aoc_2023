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

    def down(self):
        for col in range(self.width):
            for row in range(self.height).__reversed__():
                c = self.lines[row][col]
                if c == 'O':
                    r = row
                    while r+1 < self.height and self.lines[r+1][col] == '.':
                        self.lines[r+1][col] = 'O'
                        self.lines[r][col] = '.'
                        r += 1

    def left(self):
        for row in range(self.height):
            for col in range(self.width):
                p = self.lines[row][col]
                if p == 'O':
                    c = col
                    while c-1 >= 0 and self.lines[row][c-1] == '.':
                        self.lines[row][c-1] = 'O'
                        self.lines[row][c] = '.'
                        c -= 1

    def right(self):
        for row in range(self.height):
            for col in range(self.width).__reversed__():
                p = self.lines[row][col]
                if p == 'O':
                    c = col
                    while c+1 < self.width and self.lines[row][c+1] == '.':
                        self.lines[row][c+1] = 'O'
                        self.lines[row][c] = '.'
                        c += 1

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

    def cycle(self):
        self.up()
        self.left()
        self.down()
        self.right()

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

    def test_down(self):
        a = self.example()
        a.down()
        self.assertEqual(
            a.as_string(),
            ".....#...."
            "....#....#"
            "...O.##..."
            "...#......"
            "O.O....O#O"
            "O.#..O.#.#"
            "O....#...."
            "OO....OO.."
            "#OO..###.."
            "#OO.O#...O"
        )

    def test_left(self):
        a = self.example()
        a.left()
        self.assertEqual(
            a.as_string(),
            "O....#...."
            "OOO.#....#"
            ".....##..."
            "OO.#OO...."
            "OO......#."
            "O.#O...#.#"
            "O....#OO.."
            "O........."
            "#....###.."
            "#OO..#....")

    def test_right(self):
        a = self.example()
        a.right()
        self.assertEqual(
            a.as_string(),
            "....O#...."
            ".OOO#....#"
            ".....##..."
            ".OO#....OO"
            "......OO#."
            ".O#...O#.#"
            "....O#..OO"
            ".........O"
            "#....###.."
            "#..OO#....")


if __name__ == '__main__':
    unittest.main()

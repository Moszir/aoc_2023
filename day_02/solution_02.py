import dataclasses
import typing
import unittest


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            self.__games = [line.strip() for line in test_input.readlines()]

    @staticmethod
    def get_game_id(game: str) -> int:
        return int(game.split(':')[0][5:])

    @dataclasses.dataclass
    class Cubes:
        greens: int = 0
        reds: int = 0
        blues: int = 0

        def __le__(self, other: 'Solution.Cubes'):
            return self.greens <= other.greens and self.reds <= other.reds and self.blues <= other.blues

        @property
        def power(self) -> int:
            return self.greens * self.reds * self.blues

    @staticmethod
    def minimum_cubes(game: str) -> Cubes:
        cubes = Solution.Cubes()
        # Remove the "Game 13:" from the start, then the revealed subsets are separated by a ';'
        for game_set in game.split(':')[1].split(';'):
            s = game_set.strip().replace(',', '').split(' ')
            # s looks like: ['32', 'green', '4', 'red', '15', 'blue']
            for value, color in zip(s[::2], s[1::2]):
                if color == 'green':
                    cubes.greens = max(cubes.greens, int(value))
                elif color == 'red':
                    cubes.reds = max(cubes.reds, int(value))
                elif color == 'blue':
                    cubes.blues = max(cubes.blues, int(value))
        return cubes

    def solve_a(self) -> int:
        reference = self.Cubes(reds=12, greens=13, blues=14)
        return sum((
            self.get_game_id(game)
            for game in self.__games
            if self.minimum_cubes(game) <= reference))

    def solve_b(self) -> int:
        return sum((self.minimum_cubes(game).power for game in self.__games))


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(8, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(2_683, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(2_286, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(49_710, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

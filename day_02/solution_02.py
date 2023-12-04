import dataclasses
import typing
import unittest


def get_game_id(game: str) -> int:
    return int(game.split(':')[0][5:])


@dataclasses.dataclass
class Cubes:
    greens: int = 0
    reds: int = 0
    blues: int = 0

    def __le__(self, other: 'Cubes'):
        return self.greens <= other.greens and self.reds <= other.reds and self.blues <= other.blues


def minimum_cubes(game: str) -> Cubes:
    cubes = Cubes()
    # Remove the "Game 13:" from the start, then the revealed subsets are separated by a ';'
    for game_set in game.split(':')[1].split(';'):
        s = game_set.strip().replace(',', '').split(' ')
        # s looks like: ['green', '32', 'red', '4', 'blue', '15']
        for i in range(0, len(s), 2):
            if s[i+1] == 'green':
                cubes.greens = max(cubes.greens, int(s[i]))
            elif s[i+1] == 'red':
                cubes.reds = max(cubes.reds, int(s[i]))
            elif s[i+1] == 'blue':
                cubes.blues = max(cubes.blues, int(s[i]))
    return cubes


def solve_a(games: typing.List[str]) -> int:
    reference = Cubes(reds=12, greens=13, blues=14)
    return sum((
        get_game_id(game)
        for game in games
        if minimum_cubes(game) <= reference))


def power(cubes: Cubes) -> int:
    return cubes.greens * cubes.reds * cubes.blues


def solve_b(games: typing.List[str]) -> int:
    return sum((power(minimum_cubes(game)) for game in games))


class TestDay2(unittest.TestCase):
    @staticmethod
    def __get_games(file_name: str) -> typing.List[str]:
        with open(file_name) as test_input:
            return [line.strip() for line in test_input.readlines()]

    def test_get_game_id(self):
        self.assertEqual(2, get_game_id('Game 2: asdf'))
        self.assertEqual(13, get_game_id('Game 13: asdf'))
        self.assertEqual(137, get_game_id('Game 137: asdf'))

    def test_cube_le(self):
        self.assertTrue(Cubes() <= Cubes())
        self.assertTrue(Cubes() <= Cubes(1, 0, 0))
        self.assertTrue(Cubes() <= Cubes(0, 1, 0))
        self.assertTrue(Cubes() <= Cubes(0, 0, 1))
        self.assertFalse(Cubes(1, 0, 0) <= Cubes())
        self.assertFalse(Cubes(0, 1, 0) <= Cubes())
        self.assertFalse(Cubes(0, 0, 1) <= Cubes())
        self.assertTrue(Cubes(11, 12, 13) <= Cubes(11, 12, 13))
        self.assertTrue(Cubes(11, 12, 13) <= Cubes(12, 12, 14))
        self.assertTrue(Cubes(11, 12, 13) <= Cubes(12, 13, 14))

    def test_a(self):
        self.assertEqual(8, solve_a(self.__get_games('example.txt')))
        self.assertEqual(2_683, solve_a(self.__get_games('input.txt')))

    def test_b(self):
        self.assertEqual(2_286, solve_b(self.__get_games('example.txt')))
        self.assertEqual(49_710, solve_b(self.__get_games('input.txt')))


if __name__ == '__main__':
    unittest.main()

import typing
import unittest


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]
            self.matches = [self.count_matches(card) for card in lines]

    @staticmethod
    def count_matches(card: str) -> int:
        play_area = card.split(':')[1]
        winning_numbers_string = play_area.split('|')[0].strip().split(' ')
        winning_numbers = [int(x) for x in winning_numbers_string if x != '']

        played_numbers_string = play_area.split('|')[1].strip().split(' ')
        played_numbers = [int(x) for x in played_numbers_string if x != '']

        return sum((1 for x in played_numbers if x in winning_numbers))

    def solve_a(self) -> int:
        return sum((
            2**(match - 1)
            for match in self.matches
            if match > 0))

    def solve_b(self) -> int:
        copies = [1 for _ in range(len(self.matches))]
        for game_number, match in enumerate(self.matches):
            for index in range(match):
                if game_number+index+1 < len(copies):
                    copies[game_number+index+1] += copies[game_number]
        return sum(copies)


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(13, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(24_733, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(30, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(5_422_730, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

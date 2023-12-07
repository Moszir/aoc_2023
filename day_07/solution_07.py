import unittest

labels = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
b_labels = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']


class Hand:
    def __init__(self, line):
        self.hand: str = line.split(' ')[0]
        self.bid: int = int(line.split(' ')[1])

        self.type_rank = sorted([self.hand.count(label) for label in labels], reverse=True)
        self.label_rank = [labels.index(card) for card in self.hand]

        self.type_rank_b = sorted([self.hand.count(label) for label in labels if label != 'J'], reverse=True)
        self.type_rank_b[0] += self.hand.count('J')
        self.label_rank_b = [b_labels.index(card) for card in self.hand]


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]
            self.__hands = [Hand(line) for line in lines]

    def solve_a(self) -> int:
        hands = sorted(self.__hands, key=lambda hand: (hand.type_rank, hand.label_rank))
        return sum(
            (idx+1) * hand.bid
            for idx, hand in enumerate(hands))

    def solve_b(self) -> int:
        hands = sorted(self.__hands, key=lambda hand: (hand.type_rank_b, hand.label_rank_b))
        return sum(
            (idx+1) * hand.bid
            for idx, hand in enumerate(hands))


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(6440, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(246409899, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(5905, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(244848487, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

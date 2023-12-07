import unittest

labels = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
b_labels = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

hand_types = ['five', 'four', 'full', 'three', 'two pair', 'one pair', 'nothing']


class Hand:
    def __init__(self, line):
        self.hand: str = line.split(' ')[0]
        self.bid: int = int(line.split(' ')[1])

        self.type = self.rank(self.hand)
        self.type_rank = hand_types.index(self.type)
        self.label_ranks = [labels.index(card) for card in self.hand]

        self.b_type = self.b_rank(self.hand)
        self.b_type_rank = hand_types.index(self.b_type)
        self.b_label_ranks = [b_labels.index(card) for card in self.hand]

    @staticmethod
    def rank(hand):
        counts = [hand.count(label) for label in labels]
        return (
            'five' if 5 in counts else
            'four' if 4 in counts else
            'full' if 3 in counts and 2 in counts else
            'three' if 3 in counts else
            'two pair' if counts.count(2) == 2 else
            'one pair' if 2 in counts else
            'nothing')

    @staticmethod
    def b_rank(hand):
        counts = [hand.count(label) for label in labels if label != 'J']
        jokers = hand.count('J')
        if jokers in (4, 5):
            return 'five'
        elif jokers == 3:  # JJJaa or JJJab
            return 'five' if 2 in counts else 'four'
        elif jokers == 2:  # JJaaa or JJaab or JJabc
            return 'five' if 3 in counts else 'four' if 2 in counts else 'three'
        elif jokers == 1:
            # Jaaaa Jaaab Jaabb Jaabc Jabcd
            if 4 in counts:
                return 'five'
            elif 3 in counts:
                return 'four'
            elif 2 in counts and counts.count(2) == 2:
                return 'full'
            elif 2 in counts:
                return 'three'
            else:
                return 'one pair'
        else:
            # No jokers: rank normally
            return Hand.rank(hand)


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]
            self.__hands = [Hand(line) for line in lines]

    def solve_a(self) -> int:
        # Sort so that the best hand is at the end
        # The labels and hand types are listed best-to-worst, so sorting based on their indexes should be reversed.
        hands = sorted(self.__hands, key=lambda hand: (hand.type_rank, hand.label_ranks), reverse=True)
        return sum(
            (idx+1) * hand.bid
            for idx, hand in enumerate(hands))

    def solve_b(self) -> int:
        # Sort so that the best hand is at the end
        # The labels and hand types are listed best-to-worst, so sorting based on their indexes should be reversed.
        hands = sorted(self.__hands, key=lambda hand: (hand.b_type_rank, hand.b_label_ranks), reverse=True)
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

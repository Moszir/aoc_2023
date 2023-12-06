import dataclasses
import typing
import unittest


@dataclasses.dataclass
class Number:
    digit: str
    name: str
    value: int


numbers: typing.List[Number] = [
    Number('1', 'one', 1),
    Number('2', 'two', 2),
    Number('3', 'three', 3),
    Number('4', 'four', 4),
    Number('5', 'five', 5),
    Number('6', 'six', 6),
    Number('7', 'seven', 7),
    Number('8', 'eight', 8),
    Number('9', 'nine', 9),
]


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            self.__lines = [line.strip() for line in test_input.readlines()]

    @staticmethod
    def process_line(line: str, use_strings: bool) -> int:
        first = -1
        last = -1
        for idx in range(len(line)):
            for number in numbers:
                if line[idx] == number.digit or (use_strings and line[idx:idx+len(number.name)] == number.name):
                    last = number.value
                    if first == -1:
                        first = number.value
        return 10*first + last

    def solve_a(self) -> int:
        return sum((self.process_line(line, use_strings=False) for line in self.__lines))

    def solve_b(self) -> int:
        return sum((self.process_line(line, use_strings=True) for line in self.__lines))


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(142, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(55_538, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(281, Solution('example_b.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(54_875, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

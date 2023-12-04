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


def solve(lines: typing.List[str], use_strings: bool) -> int:
    return sum((process_line(line, use_strings) for line in lines))


class TestDay1(unittest.TestCase):
    @staticmethod
    def __get_test_lines() -> typing.List[str]:
        with open('input.txt') as test_input:
            return [line.strip() for line in test_input.readlines()]

    def test_process_line_digits_only(self):
        test_cases = [
            ('1', 11),
            ('1abc', 11),
            ('ab1cd', 11),
            ('abc1', 11),
            ('1abc2', 12),
            ('1ab2cd', 12),
            ('ab1cd2', 12),
            ('a1bc2d', 12),
            ('a1b3c2d', 12),
        ]
        for test_case in test_cases:
            self.assertEqual(test_case[1], process_line(test_case[0], False))

    def test_process_line(self):
        test_cases = [
            ('one', 11),
            ('oneabc', 11),
            ('abonecd', 11),
            ('abcone', 11),
            ('oneabc2', 12),
            ('1abctwo', 12),
            ('oneabctwo', 12),
            ('oneab3cd', 13),
            ('1abthreecd', 13),
            ('oneabthreecd', 13),
            ('abonecd4', 14),
            ('ab1cdfour', 14),
            ('abonecdfour', 14),
            ('aonebc5d', 15),
            ('a1bcfived', 15),
            ('aonebcfived', 15),
            ('aonebthreec6d', 16),
            ('a1bthreecsixd', 16),
            ('aonebthreecsixd', 16),
            ('aoneb3c7d', 17),
            ('a1b3csevend', 17),
            ('aoneb3csevend', 17),
        ]
        for test_case in test_cases:
            self.assertEqual(test_case[1], process_line(test_case[0], True))

    def test_a_example(self):
        lines = ['1abc2', 'pqr3stu8vwx', 'a1b2c3d4e5f', 'treb7uchet']
        self.assertEqual(142, solve(lines, False))

    def test_a(self):
        self.assertEqual(55_538, solve(self.__get_test_lines(), False))

    def test_b_example(self):
        lines = [
            'two1nine',
            'eightwothree',
            'abcone2threexyz',
            'xtwone3four',
            '4nineeightseven2',
            'zoneight234',
            '7pqrstsixteen'
        ]
        self.assertEqual(281, solve(lines, True))

    def test_b(self):
        self.assertEqual(54_875, solve(self.__get_test_lines(), True))


if __name__ == '__main__':
    unittest.main()

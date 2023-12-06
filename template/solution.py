import dataclasses
import typing
import unittest


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]

    def solve_a(self) -> int:
        return 0

    def solve_b(self) -> int:
        return 0


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(0, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(0, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(0, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(0, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

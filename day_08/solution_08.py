import dataclasses
import math
import typing
import unittest


@dataclasses.dataclass
class Node:
    left: str
    right: str


class Solution:

    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]
            self.__instructions = lines[0]
            self.__nodes = {
                line[:3]: Node(line[7:10], line[12:15])
                for line in lines[2:]
            }

    def solve_a(self) -> int:
        position = 'AAA'
        steps = 0
        while position != 'ZZZ':
            instruction = self.__instructions[steps % len(self.__instructions)]
            node = self.__nodes[position]
            if instruction == 'L':
                position = node.left
            else:
                position = node.right
            steps += 1
        return steps

    def solve_b(self) -> int:
        positions: typing.List[str] = [key for key in self.__nodes.keys() if key[-1] == 'A']
        steps = 0
        cycle_numbers: typing.Dict[int, int] = {}
        while True:
            instruction = self.__instructions[steps % len(self.__instructions)]
            steps += 1
            next_positions: typing.List[str] = []
            for index, position in enumerate(positions):
                next_position = self.__nodes[position].left if instruction == 'L' else self.__nodes[position].right
                next_positions.append(next_position)
                if next_position[-1] == 'Z':
                    cycle_numbers[index] = steps
            if len(cycle_numbers) == len(positions):  # all has a number now
                return math.lcm(*cycle_numbers.values())
            positions = next_positions


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(2, Solution('example.txt').solve_a())

    def test_a_example_2(self):
        self.assertEqual(6, Solution('example_2.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(14_893, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(6, Solution('example_b.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(10_241_191_004_509, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

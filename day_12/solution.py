import pathlib
import typing
import unittest


class Solution:
    def __init__(self, path: pathlib.Path):
        lines = path.read_text().splitlines()
        self.springs = [line.split(' ')[0] for line in lines]
        self.clues = [[int(c) for c in line.split(' ')[1].split(',')] for line in lines]

    @staticmethod
    def solve_line(line: str, clue: typing.List[int]) -> int:
        """
        Exhaustive solution with some memoization.
        Basically, it branches on every '?', but we store solutions for tail ends:

        For example:
        ?????????????????  [1, whatever]

        branching on the first 3 characters:
        ##??????????????? -> 0
        #.#??????????????
        #..??????????????       <-- this one should have the same number of solutions
        .#.??????????????       <-- as this one
        .##?????????????? -> 0
        ..#??????????????
        ...??????????????
        """
        store = {}

        def f(index, clue_index, current_block_length):
            key = (index, clue_index, current_block_length)
            if key in store:
                return store[key]

            # At the end of the line...
            if index == len(line):
                # ... and out of clues too
                if clue_index == len(clue) and current_block_length == 0:
                    return 1
                # ... and on the last clue, which matches the current block
                elif clue_index == len(clue) - 1 and clue[clue_index] == current_block_length:
                    return 1
                # otherwise that won't work.
                else:
                    return 0

            result = 0
            if line[index] == '.':
                # the current block works for the current clue?
                if clue_index < len(clue) and 0 < current_block_length == clue[clue_index]:
                    result += f(index + 1, clue_index + 1, 0)
                elif current_block_length == 0:
                    # or not in a block at all, doh
                    result += f(index + 1, clue_index, 0)
                # else:  # abort the timeline, we will return with 0
            elif line[index] == '#':
                # our block is getting bigger...
                result += f(index + 1, clue_index, current_block_length + 1)
            else:  # line[index] == '?'
                # Branch: '#' and b), or '.' and a)
                result += f(index + 1, clue_index, current_block_length + 1)
                if current_block_length == 0:
                    result += f(index + 1, clue_index, 0)
                elif clue_index < len(clue) and 0 < current_block_length == clue[clue_index]:
                    result += f(index + 1, clue_index + 1, 0)

            store[key] = result
            return result

        return f(0, 0, 0)

    def solve_a(self) -> int:
        return sum((
            self.solve_line(line, clue)
            for line, clue in zip(self.springs, self.clues)
        ))

    def solve_b(self) -> int:
        self.springs = ['?'.join((line, line, line, line, line)) for line in self.springs]
        self.clues = [[*c, *c, *c, *c, *c] for c in self.clues]
        return self.solve_a()


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(21, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(6_981, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(525_152, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(4_546_215_031_609, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

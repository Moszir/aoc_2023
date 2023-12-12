import copy
import dataclasses
import itertools
import math
import pathlib
import typing
import unittest

from moszir_utils.asterisk import *


class Solution:
    def __init__(self, path: pathlib.Path):
        lines = path.read_text().splitlines()
        self.springs = [line.split(' ')[0] for line in lines]
        self.clues = [[int(c) for c in line.split(' ')[1].split(',')] for line in lines]

    def solve_a(self) -> int:
        accu = 0
        c = 1
        for line, clue in zip(self.springs, self.clues):
            print(line, clue, f'{c} / {len(self.springs)}')
            accu += self.solve_line(line, clue)
            c += 1

        return accu

    @staticmethod
    def solve_line(line: str, clue: typing.List[int]) -> int:
        question_marks = [idx for idx, c in enumerate(line) if c == '?']
        needs = sum(clue) - sum((1 for c in line if c == '#'))
        # print(question_marks, needs)
        accu = 0
        m = math.comb(len(question_marks), needs)
        print(len(question_marks), needs, m)
        count = 0
        for p in itertools.combinations(question_marks, r=needs):
            count += 1
            if count % 1_000_000 == 0:
                print(f'{count}/{m}')
            line_try = [
                '#' if c == '#' or (c == '?' and i in p) else
                '.'
                for i, c in enumerate(line)
            ]
            # print(line_try)
            clue_try = []
            count = 0
            for c in line_try:
                if c in ('?', '#'):
                    count += 1
                else:
                    if count != 0:
                        clue_try.append(count)
                    count = 0
            if count != 0:
                clue_try.append(count)
            # print(clue_try)
            if clue == clue_try:
                accu += 1

        return accu

    def solve_b(self) -> int:
        self.springs = ['?'.join((line, line, line, line, line)) for line in self.springs]
        self.clues = [[*c, *c, *c, *c, *c] for c in self.clues]

        accu = 0
        for line, clue in zip(self.springs, self.clues):
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

                if line[index] == '.':
                    # the current block works for the current clue?
                    if clue_index < len(clue) and 0 < current_block_length == clue[clue_index]:
                        result = f(index + 1, clue_index + 1, 0)
                        store[key] = result
                        return result
                    elif current_block_length == 0:
                        # or not in a block at all, doh
                        result = f(index + 1, clue_index, 0)
                        store[key] = result
                        return result
                    else:  # abort the timeline
                        store[key] = 0
                        return 0
                elif line[index] == '#':
                    # our block is getting bigger...
                    result = f(index + 1, clue_index, current_block_length + 1)
                    store[key] = result
                    return result
                else:  # line[index] == '?'
                    # The interesting part. We can either make it a '#' and do the same as b):
                    result = f(index + 1, clue_index, current_block_length + 1)
                    # Or a '.', and do the same as a)
                    if current_block_length == 0:
                        result += f(index + 1, clue_index, 0)
                    elif clue_index < len(clue) and 0 < current_block_length == clue[clue_index]:
                        result += f(index + 1, clue_index + 1, 0)
                    store[key] = result
                    return result

            accu += f(0, 0, 0)
        return accu


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
        self.assertEqual(0, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(525152, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(4546215031609, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

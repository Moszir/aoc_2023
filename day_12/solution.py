import pathlib
import typing
import unittest

type Clue = typing.List[int]
type Clues = typing.List[Clue]


class Solution:
    def __init__(self, path: pathlib.Path):
        lines = path.read_text().splitlines()
        self.springs = [line.split(' ')[0] for line in lines]
        self.clues: Clues = [[int(c) for c in line.split(' ')[1].split(',')] for line in lines]

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
        self.springs = ['?'.join([line] * 5) for line in self.springs]
        self.clues = [clue * 5 for clue in self.clues]
        return self.solve_a()


class BasicTests(unittest.TestCase):
    def __test(self, expected: int, line: str, clue: Clue):
        self.assertEqual(expected, Solution.solve_line(line, clue))

    def test_no_blocks(self):
        self.__test(1, '.', [])
        self.__test(0, '#', [])
        self.__test(1, '?', [])

    def test_one_block(self):
        self.__test(1, '#', [1])
        self.__test(0, '.', [1])
        self.__test(1, '?', [1])
        self.__test(1, '..###....', [3])
        self.__test(1, '..?##....', [3])
        self.__test(1, '..#?#....', [3])
        self.__test(1, '..##?....', [3])
        self.__test(1, '..??#....', [3])
        self.__test(1, '..?#?....', [3])
        self.__test(1, '..#??....', [3])
        self.__test(1, '..???....', [3])
        self.__test(2, '.????....', [3])
        self.__test(7, '?????????', [3])


class ExponentialTests(unittest.TestCase):
    """A funny example for the power of memoization"""
    @staticmethod
    def repeat_line(i: int) -> str:
        return '??.' * i

    @staticmethod
    def repeat_clue(i: int) -> Clue:
        return [1] * i

    def test_test_setup(self):
        self.assertEqual('??.??.??.', self.repeat_line(3))
        self.assertEqual([1, 1, 1], self.repeat_clue(3))

    def __test(self, n: int):
        self.assertEqual(2 ** n, Solution.solve_line(self.repeat_line(n), self.repeat_clue(n)))

    def test_100(self):
        self.__test(100)  # 19ms

    def test_200(self):
        self.__test(200)  # 86ms

    def test_300(self):
        self.__test(300)  # 221ms
        # The solution is 2037035976334486086268445688409378161051468393665936250636140449354381299763336706183397376
        # print(2**300)

    # @unittest.skip('Maximum recursion depth exceeded')
    # def test_400(self):
    #     """ Homework: eliminate recursion from the algorithm. """
    #     self.__test(400)


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

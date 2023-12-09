import unittest


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]
            self.sequences = [[int(x) for x in line.split(' ')] for line in lines]

    @staticmethod
    def generate_table(sequence):
        table = [sequence]
        while any(x != 0 for x in table[-1]):
            table.append([])
            for i in range(len(table[-2])-1):
                table[-1].append(table[-2][i+1] - table[-2][i])
        return table

    def extrapolate(self, sequence):
        return sum((row[-1] for row in self.generate_table(sequence)))

    def extrapolate_back(self, sequence):
        first_column = [row[0] for row in self.generate_table(sequence)]
        return sum((a-b for a, b in zip(first_column[0::2], first_column[1::2])))  # a0 - a1 + a2 - a3 + ...

    def solve_a(self) -> int:
        return sum((self.extrapolate(sequence) for sequence in self.sequences))

    def solve_b(self) -> int:
        return sum((self.extrapolate_back(sequence) for sequence in self.sequences))


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(114, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(1789635132, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(2, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(913, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

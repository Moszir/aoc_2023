import pathlib
import unittest


class Solution:
    def __init__(self, path: pathlib.Path):
        self.entries = path.read_text().split(',')

    @staticmethod
    def hash(word: str):
        accu = 0
        for c in word:
            accu += ord(c)
            accu *= 17
            accu %= 256
        return accu

    def solve_a(self) -> int:
        return sum((self.hash(entry) for entry in self.entries))

    def solve_b(self) -> int:
        boxes = [[] for _ in range(256)]
        for entry in self.entries:
            if entry[-1] == '-':
                name = entry[:-1]
                index = self.hash(name)
                boxes[index] = [lens for lens in boxes[index] if lens[0] != name]
            else:
                name = entry.split('=')[0]
                focal = int(entry.split('=')[1])
                box = boxes[self.hash(name)]
                lens = next((lens for lens in box if lens[0] == name), None)
                if lens is None:
                    box.append([name, focal])
                else:
                    lens[1] = focal

        accu = 0
        for i, box in enumerate(boxes):
            for j, lens in enumerate(box):
                accu += (i+1) * (j+1) * lens[1]
        return accu


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(1320, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(502_139, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(145, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(284_132, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

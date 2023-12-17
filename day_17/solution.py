import pathlib
import unittest
import heapq

from moszir_utils.asterisk import *
from moszir_utils.asterisk import Position as P


class Solution:
    def __init__(self, path: pathlib.Path):
        self.map = Table.from_table([[int(c) for c in line] for line in path.read_text().splitlines()])
        self.height = self.map.height
        self.width = self.map.width

    def solve(self, *, min_to_turn: int = 0, max_without_turn: int) -> int:
        dist = Table(height=self.height, width=self.width)
        for p in dist.positions():
            dist[p] = {}
        q = [(0, P(0, 0), P(1, 0), 0), (0, P(0, 0), P(0, 1), 0)]  # value, position, direction, so far
        while q:
            value, pos, d, so_far = heapq.heappop(q)
            go = [(P(d.c, d.r), 1), (P(-d.c, -d.r), 1)] if so_far >= min_to_turn else []
            if so_far < max_without_turn:
                go.append((d, so_far+1))
            for new_dir, new_so_far in go:
                new_pos = pos+new_dir
                if self.map.valid_index(new_pos):
                    new_v = value + self.map[new_pos]
                    key = (new_dir, new_so_far)
                    if key not in dist[new_pos] or new_v < dist[new_pos][key]:
                        dist[new_pos][key] = new_v
                        heapq.heappush(q, (new_v, new_pos, *key))

        return min(dist[P(self.height-1, self.width-1)].values())

    def solve_a(self) -> int:
        return self.solve(max_without_turn=3)

    def solve_b(self) -> int:
        return self.solve(min_to_turn=4, max_without_turn=10)


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(102, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(686, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(94, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(801, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

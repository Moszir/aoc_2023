import copy
import dataclasses
import itertools
import math
import pathlib
import typing
import unittest
import heapq

from moszir_utils.asterisk import *


class Solution:
    def __init__(self, path: pathlib.Path):
        self.map = [[int(c) for c in line] for line in path.read_text().splitlines()]
        self.height = len(self.map)
        self.width = len(self.map)

    def solve_a(self) -> int:
        # print(self.map)
        dist = [[{} for c in line] for line in self.map]
        dist[0][0][('right', 0)] = 0
        dist[0][0][('down', 0)] = 0
        q = [(0, (0, 0, ('right', 0))), (0, (0, 0, ('down', 0)))]  # value, coordinate, sort after adding stuff!
        while q:
            p = heapq.heappop(q)
            v, (x, y, (direction, so_far)) = p
            if direction == 'right':
                if x > 0:  # go up
                    w = v + self.map[x-1][y]
                    nd = ('up', 1)
                    if nd not in dist[x-1][y]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
                    elif w < dist[x-1][y][nd]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
                if x+1 < self.height:  # go down
                    w = v + self.map[x+1][y]
                    nd = ('down', 1)
                    if nd not in dist[x+1][y]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))
                    elif w < dist[x+1][y][nd]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))
                if y+1 < self.width and so_far < 3:
                    w = v + self.map[x][y+1]
                    nd = ('right', so_far+1)
                    if nd not in dist[x][y+1]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
                    elif w < dist[x][y+1][nd]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
            if direction == 'left':
                if x > 0:  # go up
                    w = v + self.map[x-1][y]
                    nd = ('up', 1)
                    if nd not in dist[x-1][y]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
                    elif w < dist[x-1][y][nd]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
                if x+1 < self.height:  # go down
                    w = v + self.map[x+1][y]
                    nd = ('down', 1)
                    if nd not in dist[x+1][y]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))
                    elif w < dist[x+1][y][nd]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))
                if y-1 >= 0 and so_far < 3:
                    w = v + self.map[x][y-1]
                    nd = ('left', so_far+1)
                    if nd not in dist[x][y-1]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
                    elif w < dist[x][y-1][nd]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
            if direction == 'up':
                if y > 0:  # go left
                    w = v + self.map[x][y-1]
                    nd = ('left', 1)
                    if nd not in dist[x][y-1]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
                    elif w < dist[x][y-1][nd]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
                if y+1 < self.width:  # go right
                    w = v + self.map[x][y+1]
                    nd = ('right', 1)
                    if nd not in dist[x][y+1]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
                    elif w < dist[x][y+1][nd]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
                if x-1 >= 0 and so_far < 3:
                    w = v + self.map[x-1][y]
                    nd = ('up', so_far+1)
                    if nd not in dist[x-1][y]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
                    elif w < dist[x-1][y][nd]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
            if direction == 'down':
                if y > 0:  # go left
                    w = v + self.map[x][y-1]
                    nd = ('left', 1)
                    if nd not in dist[x][y-1]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
                    elif w < dist[x][y-1][nd]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
                if y+1 < self.width:  # go right
                    w = v + self.map[x][y+1]
                    nd = ('right', 1)
                    if nd not in dist[x][y+1]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
                    elif w < dist[x][y+1][nd]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
                if x+1 < self.height and so_far < 3:
                    w = v + self.map[x+1][y]
                    nd = ('down', so_far+1)
                    if nd not in dist[x+1][y]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))
                    elif w < dist[x+1][y][nd]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))

        return min(dist[self.height-1][self.width-1].values())

    def solve_b(self) -> int:
        dist = [[{} for c in line] for line in self.map]
        dist[0][0][('right', 0)] = 0
        dist[0][0][('down', 0)] = 0
        q = [(0, (0, 0, ('right', 0))), (0, (0, 0, ('down', 0)))]  # value, coordinate, sort after adding stuff!
        while q:
            if len(q) % 100 == 0:
                print(len(q))
            p = heapq.heappop(q)
            v, (x, y, (direction, so_far)) = p
            if direction == 'right':
                if x > 0 and so_far >= 4:  # go up
                    w = v + self.map[x-1][y]
                    nd = ('up', 1)
                    if nd not in dist[x-1][y]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
                    elif w < dist[x-1][y][nd]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
                if x+1 < self.height and so_far >= 4:  # go down
                    w = v + self.map[x+1][y]
                    nd = ('down', 1)
                    if nd not in dist[x+1][y]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))
                    elif w < dist[x+1][y][nd]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))
                if y+1 < self.width and so_far < 10:
                    w = v + self.map[x][y+1]
                    nd = ('right', so_far+1)
                    if nd not in dist[x][y+1]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
                    elif w < dist[x][y+1][nd]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
            if direction == 'left':
                if x > 0 and so_far >= 4:  # go up
                    w = v + self.map[x-1][y]
                    nd = ('up', 1)
                    if nd not in dist[x-1][y]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
                    elif w < dist[x-1][y][nd]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
                if x+1 < self.height and so_far >= 4:  # go down
                    w = v + self.map[x+1][y]
                    nd = ('down', 1)
                    if nd not in dist[x+1][y]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))
                    elif w < dist[x+1][y][nd]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))
                if y-1 >= 0 and so_far < 10:
                    w = v + self.map[x][y-1]
                    nd = ('left', so_far+1)
                    if nd not in dist[x][y-1]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
                    elif w < dist[x][y-1][nd]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
            if direction == 'up':
                if y > 0 and so_far >= 4:  # go left
                    w = v + self.map[x][y-1]
                    nd = ('left', 1)
                    if nd not in dist[x][y-1]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
                    elif w < dist[x][y-1][nd]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
                if y+1 < self.width and so_far >= 4:  # go right
                    w = v + self.map[x][y+1]
                    nd = ('right', 1)
                    if nd not in dist[x][y+1]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
                    elif w < dist[x][y+1][nd]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
                if x-1 >= 0 and so_far < 10:
                    w = v + self.map[x-1][y]
                    nd = ('up', so_far+1)
                    if nd not in dist[x-1][y]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
                    elif w < dist[x-1][y][nd]:
                        dist[x-1][y][nd] = w
                        heapq.heappush(q, (w, (x-1, y, nd)))
            if direction == 'down':
                if y > 0 and so_far >= 4:  # go left
                    w = v + self.map[x][y-1]
                    nd = ('left', 1)
                    if nd not in dist[x][y-1]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
                    elif w < dist[x][y-1][nd]:
                        dist[x][y-1][nd] = w
                        heapq.heappush(q, (w, (x, y-1, nd)))
                if y+1 < self.width and so_far >= 4:  # go right
                    w = v + self.map[x][y+1]
                    nd = ('right', 1)
                    if nd not in dist[x][y+1]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
                    elif w < dist[x][y+1][nd]:
                        dist[x][y+1][nd] = w
                        heapq.heappush(q, (w, (x, y+1, nd)))
                if x+1 < self.height and so_far < 10:
                    w = v + self.map[x+1][y]
                    nd = ('down', so_far+1)
                    if nd not in dist[x+1][y]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))
                    elif w < dist[x+1][y][nd]:
                        dist[x+1][y][nd] = w
                        heapq.heappush(q, (w, (x+1, y, nd)))

        return min(dist[self.height-1][self.width-1].values())


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

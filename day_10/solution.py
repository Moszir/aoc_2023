import dataclasses
import typing
import unittest

from moszir_utils.position import Position
from moszir_utils.table import Table


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            self.map = Table.from_lines([line.strip() for line in test_input.readlines()])

    @staticmethod
    def match_horizontally(left: str, right: str) -> bool:
        return left in ('S', 'L', '-', 'F') and right in ('S', 'J', '-', '7')

    @staticmethod
    def match_vertically(up: str, down: str) -> bool:
        return up in ('S', '7', '|', 'F') and down in ('S', 'J', '|', 'L')

    def neighbors(self, position: Position) -> typing.List[Position]:
        value = self.map[position]
        result = []
        if self.match_vertically(self.map[position.up], value):
            result.append(position.up)
        if self.match_vertically(value, self.map[position.down]):
            result.append(position.down)
        if self.match_horizontally(self.map[position.left], value):
            result.append(position.left)
        if self.match_horizontally(value, self.map[position.right]):
            result.append(position.right)
        return result

    def find_main_loop(self) -> typing.List[Position]:
        start = self.map.find_first('S')
        assert start is not None

        q = [(start, None)]  # position, predecessor
        predecessor: typing.Dict[Position, typing.Optional[Position]] = {start: None}
        while len(q) > 0:
            p, pred = q.pop()
            ns = self.neighbors(p)
            for n in ns:
                if n == pred:
                    continue
                if n not in predecessor.keys():
                    q.append((n, p))
                    predecessor[n] = p
                else:
                    # collect from n and p
                    result = []
                    while n is not None:
                        result.append(n)
                        n = predecessor[n]
                    while p is not None:
                        result.append(p)
                        p = predecessor[p]
                    result.pop()  # added start twice
                    return result

    def solve_a(self) -> int:
        # The main loop will be 0 -> 1 -> ... -> N-1 -> N
        #                       L -> 1 -> ... -> N-1 -- J
        # Therefore the length of the loop is 2N.
        return len(self.find_main_loop()) // 2

    def solve_b(self) -> int:
        # Remove the pipes outside the main loop
        main_loop = set(self.find_main_loop())
        for row_index in range(self.map.height):
            for column_index in range(self.map.width):
                position = Position(row=row_index, column=column_index)
                if position not in main_loop:
                    self.map[position] = '.'

        # Blow up everything twice the size, so the pipes don't "touch"
        # Make sure there is an empty row and column around the map to flood from.
        def blow(original: Position) -> Position:
            return Position(row=2*original.row+1, column=2*original.column+1)

        blow_rows = 2*self.map.height+1
        blow_columns = 2*self.map.width+1
        blow_map = Table(height=blow_rows, width=blow_columns, default_content='.')
        for position in self.map.positions():
            value = self.map[position]
            blow_position = blow(position)
            blow_map[blow_position] = value
            if self.match_horizontally(value, self.map[position.right]):
                blow_map[blow_position.right] = '-'
            if self.match_vertically(value, self.map[position.down]):
                blow_map[blow_position.down] = '|'

        # Flood from the outside
        q = [Position(0, 0)]
        while len(q) > 0:
            p = q.pop()
            if blow_map[p] == '.':
                blow_map[p] = '*'
                q.extend(p.neighbors)
        # blow_map.print()

        # Count the "dry spots"
        return sum(
            1
            for position in self.map.positions()
            if blow_map[blow(position)] == '.')


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(8, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(6701, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(1, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(303, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

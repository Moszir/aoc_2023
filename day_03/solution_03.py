import dataclasses
import typing
import unittest


class EngineMap:
    def __init__(self, engine_map: typing.List[str]):
        self.__map = engine_map

    @property
    def number_of_rows(self):
        return len(self.__map)

    @property
    def number_of_columns(self):
        return len(self.__map[0])

    @dataclasses.dataclass
    class Result:
        number: int = 0
        size: int = 0

    def read_number(self, row_index: int, column_index: int) -> Result:
        result = EngineMap.Result()
        row = self.__map[row_index]
        while column_index + result.size < self.number_of_columns and row[column_index:column_index+result.size+1].isdigit():
            result.size += 1
        if result.size > 0:
            result.number = int(row[column_index:column_index+result.size])
        return result

    def neighbor_cells(self, row_index: int, column_index: int, size: int) -> typing.List[typing.Tuple[int, int]]:
        result = []
        start_index = column_index-1 if column_index > 0 else column_index
        end_index = column_index+size if column_index+size < self.number_of_columns else column_index+size-1
        if row_index-1 >= 0:
            result.extend(((row_index-1, index) for index in range(start_index, end_index+1)))
        if row_index+1 < self.number_of_rows:
            result.extend(((row_index+1, index) for index in range(start_index, end_index+1)))
        if column_index-1 >= 0:
            result.append((row_index, column_index-1))
        if column_index+size < self.number_of_columns:
            result.append((row_index, column_index+size))
        return result

    def solve_a(self) -> int:
        def is_symbol(c) -> bool:
            return not c.isdigit() and c != '.'

        part_number_sum = 0
        for row_index in range(self.number_of_rows):
            column_index = 0
            while column_index < self.number_of_columns:
                result = self.read_number(row_index=row_index, column_index=column_index)
                if result.size > 0:
                    neighbors = self.neighbor_cells(row_index=row_index, column_index=column_index, size=result.size)
                    if any((is_symbol(self.__map[cell[0]][cell[1]]) for cell in neighbors)):
                        part_number_sum += result.number
                column_index += result.size + 1

        return part_number_sum

    def solve_b(self) -> int:
        gear_map = [
            [[] for _ in range(self.number_of_columns)]
            for _ in range(self.number_of_rows)]

        for row_index in range(self.number_of_rows):
            column_index = 0
            while column_index < self.number_of_columns:
                result = self.read_number(row_index=row_index, column_index=column_index)
                if result.size > 0:
                    for cell in self.neighbor_cells(row_index=row_index, column_index=column_index, size=result.size):
                        if self.__map[cell[0]][cell[1]] == '*':
                            gear_map[cell[0]][cell[1]].append(result.number)
                column_index += result.size + 1

        return sum((
            gear[0] * gear[1]
            for row in gear_map
            for gear in row
            if len(gear) == 2))


class TestDay3(unittest.TestCase):
    @staticmethod
    def __get_map(file_name: str) -> typing.List[str]:
        with open(file_name) as test_input:
            return [line.strip() for line in test_input.readlines()]

    def test_a(self):
        self.assertEqual(4_361, EngineMap(self.__get_map('example.txt')).solve_a())
        self.assertEqual(540_212, EngineMap(self.__get_map('input.txt')).solve_a())

    def test_b(self):
        self.assertEqual(467_835, EngineMap(self.__get_map('example.txt')).solve_b())
        self.assertEqual(87_605_697, EngineMap(self.__get_map('input.txt')).solve_b())


if __name__ == '__main__':
    unittest.main()


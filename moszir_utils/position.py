import dataclasses
import typing


class Position(typing.NamedTuple):
    r: int  # row
    c: int  # column

    def __add__(self, other) -> 'Position':
        return Position(self.r + other.r, self.c + other.c)

    def __hash__(self):
        return (self.r, self.c).__hash__()

    @property
    def up(self) -> 'Position':
        return Position(self.r - 1, self.c)

    @property
    def down(self) -> 'Position':
        return Position(self.r + 1, self.c)

    @property
    def left(self) -> 'Position':
        return Position(self.r, self.c - 1)

    @property
    def right(self) -> 'Position':
        return Position(self.r, self.c + 1)

    @property
    def neighbors(self) -> typing.List['Position']:
        return [self.up, self.right, self.down, self.left]

    @classmethod
    def manhattan_distance(cls, point1: 'Position', point2: 'Position') -> int:
        return abs(point1.r - point2.r) + abs(point1.c - point2.c)

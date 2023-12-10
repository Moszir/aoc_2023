import dataclasses
import typing


@dataclasses.dataclass
class Position:
    row: int
    column: int

    def __hash__(self):
        return (self.row, self.column).__hash__()

    @property
    def up(self) -> 'Position':
        return Position(self.row-1, self.column)

    @property
    def down(self) -> 'Position':
        return Position(self.row+1, self.column)

    @property
    def left(self) -> 'Position':
        return Position(self.row, self.column-1)

    @property
    def right(self) -> 'Position':
        return Position(self.row, self.column+1)

    @property
    def neighbors(self) -> typing.List['Position']:
        return [self.up, self.right, self.down, self.left]

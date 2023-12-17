import typing

from moszir_utils.position import Position


class StringTable:
    """ Immutable rectangular character table. """
    def __init__(self, lines: typing.List[str]):
        assert len(lines) > 0
        assert all((len(line) == len(lines[0]) for line in lines))
        self.__table = lines
        self.__height = len(lines)
        self.__width = len(lines[0])

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    def valid_index(self, position: Position) -> bool:
        return 0 <= position.r < self.height and 0 <= position.c < self.width

    def __getitem__(self, position: Position):
        """ Unchecked indexing """
        return self.__table[position.r][position.c]

    def get(self, position: Position, default_value: typing.Any = None):
        """ Checked indexing, with default value """
        if self.valid_index(position):
            return self.__table[position.r][position.c]
        return default_value

    def print(self) -> None:
        for row in self.__table:
            print(row)

    def positions(self) -> typing.Iterable[Position]:
        return (
            Position(row, column)
            for row in range(self.height)
            for column in range(self.width))

    def top(self) -> typing.Iterable[Position]:
        return (
            Position(0, column)
            for column in range(self.width))

    def bottom(self) -> typing.Iterable[Position]:
        return (
            Position(self.height-1, column)
            for column in range(self.width))

    def left(self) -> typing.Iterable[Position]:
        return (
            Position(row, 0)
            for row in range(self.height))

    def right(self) -> typing.Iterable[Position]:
        return (
            Position(row, self.width-1)
            for row in range(self.height))

import typing

from moszir_utils.position import Position


class Table:
    def __init__(self, height: int, width: int, default_content=None):
        self.__height = height
        self.__width = width
        self.__table = [[default_content for _ in range(width)] for _ in range(height)]

    @classmethod
    def from_lines(cls, lines: typing.List[str]) -> 'Table':
        assert len(lines) > 0
        assert all((len(line) == len(lines[0]) for line in lines))
        m = Table(height=len(lines), width=len(lines[0]))
        m.__table = [[c for c in line] for line in lines]
        return m

    @classmethod
    def from_table(cls, table) -> 'Table':
        m = Table(height=len(table), width=len(table[0]))
        m.__table = table
        return m

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    def valid_index(self, position: Position) -> bool:
        return 0 <= position.r < self.__height and 0 <= position.c < self.__width

    def __getitem__(self, position: Position):
        """ Unchecked indexing """
        return self.__table[position.r][position.c]

    def get(self, position: Position, default_value: typing.Any = None):
        """ Checked indexing, with default value """
        if self.valid_index(position):
            return self.__table[position.r][position.c]
        return default_value

    def __setitem__(self, position: Position, value):
        """ Unchecked setter. Throws if out of bounds. """
        self.__table[position.r][position.c] = value

    def put(self, position: Position, value) -> None:
        """ Checked setter. Nothing happens if out of bounds. """
        if self.valid_index(position):
            self[position] = value

    def find_first(self, value) -> typing.Optional[Position]:
        for r in range(self.height):
            for c in range(self.width):
                if self.__table[r][c] == value:
                    return Position(r, c)
        return None

    def find_max_int(self) -> typing.Tuple[typing.Optional[Position], int]:
        position = None
        value = -1
        for r in range(self.height):
            for c in range(self.width):
                v = self.__table[r][c]
                if isinstance(v, int) and v > value:
                    position = Position(r, c)
                    value = v
        return position, value

    def print(self) -> None:
        for row in self.__table:
            print(''.join(c for c in row))

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

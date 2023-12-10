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

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    def __getitem__(self, position: Position):
        if 0 <= position.row < self.height and 0 <= position.column < self.width:
            return self.__table[position.row][position.column]
        return None

    def get(self, position: Position):
        return self[position]

    def __setitem__(self, position: Position, value):
        self.__table[position.row][position.column] = value

    def put(self, position: Position, value) -> None:
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

    # def positions(self) -> typing.List[Position]:
    def positions(self) -> typing.Iterable[Position]:
        return (
            Position(row=row, column=column)
            for row in range(self.height)
            for column in range(self.width)
        )

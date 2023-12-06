import dataclasses
import typing
import unittest


@dataclasses.dataclass
class Segment:
    a: int
    b: int  # left and right-inclusive!

    @staticmethod
    def from_start_and_size(start: int, size: int) -> 'Segment':
        return Segment(start, start+size-1)


Segments = typing.List[Segment]


@dataclasses.dataclass
class MappingResult:
    done: typing.Optional[Segment] = None
    remains: typing.Optional[typing.List[Segment]] = None


@dataclasses.dataclass
class MapSegment:
    a: int
    b: int  # left and right-inclusive!
    y: int  # start of the range

    # assumes that segment is in [a, b]
    def map(self, segment: Segment) -> Segment:
        return Segment(self.y + segment.a-self.a, self.y + segment.b-self.a)

    def intersect(self, segment: Segment) -> MappingResult:
        result = MappingResult()
        a, b = segment.a, segment.b
        c, d = self.a, self.b
        # Don't miss any cases:
        # - We know that a <= b and c <= d
        # - Where is `a` relative to ---c--d--- (3 cases)
        # - Where is `b` relative to the established relation of a,c,d (max 3 subcases).
        if a < c:
            if b < c:  # a <= b < c
                result.remains = [segment]
            elif b <= d:  # a < c <= b <= d
                result.remains = [Segment(a, c-1)]
                result.done = self.map(Segment(c, b))
            else:  # a < c <= d < b
                result.remains = [Segment(a, c-1), Segment(d+1, b)]
                result.done = self.map(Segment(c, d))
        elif a <= d:  # c <= a <= d
            if b <= d:  # c <= a <= b <= d
                result.done = self.map(Segment(a, b))
            else:  # c <= a <= d < b
                result.remains = [Segment(d+1, b)]
                result.done = self.map(Segment(a, d))
        else:  # d < a
            # No intersection
            result.remains = [segment]
        return result


Level = typing.List[MapSegment]


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]
            self.__seeds = [int(x) for x in lines[0].split(' ')[1:]]
            self.__levels: typing.List[Level] = []
            for line in lines[1:]:
                if line == '':  # There is a new level coming
                    self.__levels.append([])
                elif not line[0].isdigit():  # Description of the level -> ignore
                    continue
                else:
                    p = [int(x) for x in line.split(' ')]
                    self.__levels[-1].append(MapSegment(y=p[0], a=p[1], b=p[1] + p[2] - 1))

    def process_segments(self, segments: Segments) -> Segments:
        for level in self.__levels:
            resulting_segments: typing.List[Segment] = []
            for map_segment in level:
                remaining_segments: typing.List[Segment] = []
                for segment in segments:
                    result = map_segment.intersect(segment)
                    if result.done is not None:
                        resulting_segments.append(result.done)
                    if result.remains is not None:
                        remaining_segments.extend(result.remains)
                segments = remaining_segments  # Retry these segments with the next map
            # The segments that are still in `segments` map to themselves
            segments.extend(resulting_segments)
        return segments

    def solve_a(self) -> int:
        segments = [Segment(seed, seed) for seed in self.__seeds]
        return min((segment.a for segment in self.process_segments(segments)))

    def solve_b(self) -> int:
        segments = [
            Segment.from_start_and_size(self.__seeds[i], self.__seeds[i+1])
            for i in range(0, len(self.__seeds), 2)]
        return min((segment.a for segment in self.process_segments(segments)))


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(35, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(388_071_289, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(46, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(84_206_669, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()

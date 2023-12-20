from collections import defaultdict, deque
import math
import pathlib
import typing
import unittest
import enum


class Beam(enum.Enum):
    LOW = 0
    HIGH = 1


class Task(typing.NamedTuple):
    source: str
    destination: str
    beam: Beam


type Tasks = typing.List[Task]


class Broadcaster:
    def __init__(self, s):
        self.name = 'broadcaster'
        self.targets = s.split(' -> ')[1].split(', ')

    def process(self, source: str, beam: Beam) -> Tasks:
        return [Task('broadcaster', d, beam) for d in self.targets]


class FlipFlop:
    def __init__(self, s):
        self.name = s.split(' -> ')[0].strip()[1:]
        self.targets = s.split(' -> ')[1].split(', ')
        self.sends = Beam.LOW

    def process(self, source: str, beam: Beam) -> Tasks:
        if beam == Beam.HIGH:
            return []
        self.sends = Beam.LOW if self.sends == Beam.HIGH else Beam.HIGH
        return [Task(self.name, d, self.sends) for d in self.targets]


class Conjunction:
    def __init__(self, s):
        self.name = s.split(' -> ')[0].strip()[1:]
        self.targets = s.split(' -> ')[1].split(', ')
        self.memory = {}  # needs init

    def process(self, source: str, beam: Beam) -> Tasks:
        self.memory[source] = beam
        low = all((b == Beam.HIGH for b in self.memory.values()))
        b = Beam.LOW if low else Beam.HIGH
        return [Task(self.name, d, b) for d in self.targets]

    def add_source(self, name):
        self.memory[name] = Beam.LOW


class Output:
    def __init__(self):
        self.name = 'output'
        self.targets = []

    def process(self, source: str, beam: Beam) -> Tasks:
        return []


class Solution:
    def __init__(self, path: pathlib.Path):
        self.instances = [Output(), FlipFlop('%rx -> output')]
        for line in path.read_text().splitlines():
            if line[0] == '%':
                self.instances.append(FlipFlop(line))
            elif line[0] == '&':
                self.instances.append(Conjunction(line))
            elif line.startswith('broadcaster'):
                self.instances.append(Broadcaster(line))
        for i in self.instances:
            for d in i.targets:
                di = self.find_instance(d)
                if di is not None:
                    if isinstance(di, Conjunction):
                        di.add_source(i.name)

    def find_instance(self, name):
        return next((i for i in self.instances if i.name == name), None)

    def push(self) -> typing.Tuple[int, int]:
        q: Tasks = [Task('button', 'broadcaster', Beam.LOW)]
        low, high = (0, 0)
        while q:
            t = q.pop(0)
            i = self.find_instance(t.destination)
            if i is None:
                continue
            if t.beam == Beam.LOW:
                low += 1
            else:
                high += 1
            q.extend(i.process(t.source, t.beam))
        return low, high

    def solve_a(self) -> int:
        low, high = (0, 0)
        for _ in range(1_000):
            l, h = self.push()
            low += l
            high += h
        return low * high


def solve_b() -> int:
    with open('input.txt') as f:
        lines = f.read().strip().split('\n')

    # prepend the type modifier to the targets
    mt = {}
    targets = {}
    for line in lines:
        src, dest = line.split(' -> ')
        targets[src] = dest.split(', ')
        mt[src[1:]] = src[0]
    for x, ys in targets.items():
        targets[x] = [mt[y] + y if y in mt else y for y in ys]  # { '%fp': [ '%pp', '&km', ... ], ... }

    input_beam = {}  # for conjunctions: input_beam['&km'][a] is the input beam from 'a' to '&km': 'lo' or 'hi'.
    sources = defaultdict(list)
    for x, ys in targets.items():
        for y in targets[x]:
            if y[0] == '&':
                if y not in input_beam:
                    input_beam[y] = {}
                input_beam[y][x] = 'lo'
            sources[y].append(x)

    assert len(sources['rx']) == 1
    assert sources['rx'][0][0] == '&'  # There is a NAND into rx
    assert len(sources[sources['rx'][0]]) == 4  # That NAND has 4 sources
    for y in sources[sources['rx'][0]]:
        print(y)
        for z in sources[y]:
            print('  ', z)
            for w in sources[z]:
                print('    ', w)
    watch = sources[sources['rx'][0]]

    currently_high_flip_flops = set()
    previous_index = {}
    seen = defaultdict(int)
    cycle_counts = []
    for t in range(1, 10 ** 8):
        Q = deque()
        Q.append(('broadcaster', 'button', 'lo'))  # start with `button low --> broadcaster`.

        while Q:
            x, from_, typ = Q.popleft()

            if typ == 'lo':
                # Assume &df -> rx AND &a -> df, &b -> df, etc.
                # We want to know when &a,&b get 'lo' input, because then they will send a 'hi' input to &df
                # When will &df get lo inputs from all of them?
                # Assume that they get lo inputs on a perfect cycle and that df must get a 'hi' input from all of them
                # on the same timestamp. I assume they get a lot of 'hi' inputs on other timestamps that "reset" them?
                if x in previous_index and seen[x] == 2 and x in watch:
                    cycle_counts.append(t - previous_index[x])
                previous_index[x] = t
                seen[x] += 1
            if len(cycle_counts) == len(watch):
                return math.lcm(*cycle_counts)

            if x not in targets:
                continue
            if x == 'broadcaster':
                Q.extend((y, x, typ) for y in targets[x])
            elif x[0] == '%':
                if typ == 'lo':
                    if x in currently_high_flip_flops:
                        currently_high_flip_flops.discard(x)
                        new_typ = 'lo'
                    else:
                        currently_high_flip_flops.add(x)
                        new_typ = 'hi'
                    Q.extend((y, x, new_typ) for y in targets[x])
            elif x[0] == '&':
                input_beam[x][from_] = typ
                new_typ = ('lo' if all(y == 'hi' for y in input_beam[x].values()) else 'hi')
                Q.extend((y, x, new_typ) for y in targets[x])


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(11687500, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(814934624, self.real_input().solve_a())

    def test_b_input(self):
        self.assertEqual(228282646835717, solve_b())


if __name__ == '__main__':
    unittest.main()

""" This solution is incomplete!

There was an omission in the problem description of the first part of the problem description.
"""

import copy
import dataclasses
import itertools
import math
import pathlib
import typing
import unittest
import enum

from moszir_utils.asterisk import *

# %: flip-flop: turns on-off with low pulse, ignores high
#   on: sends a high pulse
#   off: sends a low pulse
# &: conjunction: remembers its two inputs, initially (low, low)
#    receives something -> remembers it, sends high if both is low, otherwise lo
# broadcast: input -> repeats it to all its targets
# BFS handling


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
        print('broadcaster', self.targets)

    def process(self, source: str, beam: Beam) -> Tasks:
        # for d in self.targets:
        #     print('broadcaster', beam, '->', d)
        return [Task('broadcaster', d, beam) for d in self.targets]


class FlipFlop:
    def __init__(self, s):
        self.name = s.split(' -> ')[0].strip()[1:]
        self.targets = s.split(' -> ')[1].split(', ')
        self.sends = Beam.LOW
        print('ff ', self.name, self.targets)

    def process(self, source: str, beam: Beam) -> Tasks:
        if beam == Beam.HIGH:
            return []
        self.sends = Beam.LOW if self.sends == Beam.HIGH else Beam.HIGH
        # for d in self.targets:
        #     print(self.name, self.sends, '->', d)
        return [Task(self.name, d, self.sends) for d in self.targets]


class Conjunction:
    def __init__(self, s):
        self.name = s.split(' -> ')[0].strip()[1:]
        self.targets = s.split(' -> ')[1].split(', ')
        self.memory = {}  # needs init
        print('&& ', self.name, self.targets)

    def process(self, source: str, beam: Beam) -> Tasks:
        self.memory[source] = beam
        low = all((b == Beam.HIGH for b in self.memory.values()))
        b = Beam.LOW if low else Beam.HIGH
        # for d in self.targets:
        #     print(self.name, b, '->', d)
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
        self.instances = [Output()]
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
        if next((i for i in self.instances if i.name == name), None) is None:
            print(name)
            print(name)
            print(name)

        return next((i for i in self.instances if i.name == name), None)

    def push(self) -> typing.Tuple[int, int]:
        q: Tasks = [Task('button', 'broadcaster', Beam.LOW)]
        low = 0
        high = 0
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
        # print('')
        return low, high

    def solve_a(self) -> int:
        low, high = (0, 0)
        for _ in range(1000):
            l, h = self.push()
            low += l
            high += h
        print(low, high)
        return low * high

    def solve_b(self) -> int:
        return 0


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
        self.assertEqual(0, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(0, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(0, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

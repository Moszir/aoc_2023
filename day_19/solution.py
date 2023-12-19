import copy
import dataclasses
import itertools
import math
import pathlib
import typing
import unittest

from moszir_utils.asterisk import *


class Condition:
    def __init__(self, s):
        self.value = None
        self.what = None
        self.to = None
        self.type = ('le' if '<' in s else 'gr' if '>' in s else 'fin')
        if self.type in ('le', 'gr'):
            self.what = ['x', 'm', 'a', 's'].index(s[0])
            self.value = int(s.split(':')[0][2:])
            self.to = s.split(':')[1]
        else:
            self.to = s


class WorkFlow:
    def __init__(self, line):
        self.name = line.split('{')[0]
        self.steps = [Condition(s) for s in line.split('{')[1][:-1].split(',')]

    def process(self, i):
        # # print(self.name, " processing ", i)
        for step in self.steps:
            if step.type == 'le':
                # # print(step.what, step.value)
                if i[step.what] < step.value:
                    return step.to
            elif step.type == 'gr':
                # # print(step.what, step.value)
                if i[step.what] > step.value:
                    return step.to
            else:
                return step.to

    def process2(self, i: typing.List[typing.List[int]]):
        tasks = []
        i = copy.deepcopy(i)
        # print(self.name, " processing ", i)
        for step in self.steps:
            if step.type == 'le':
                # print('le')
                if i[step.what][1] < step.value:
                    tasks.append((step.to, copy.deepcopy(i)))
                elif i[step.what][0] >= step.value:
                    continue
                else:
                    # print('3')
                    j = copy.deepcopy(i)
                    j[step.what][1] = step.value-1
                    # print(j, " -> ", step.to)
                    tasks.append((step.to, j))
                    i[step.what][0] = step.value  # goes through
                    # print(i, " next step")
            elif step.type == 'gr':
                # print('gr')
                if i[step.what][0] > step.value:
                    # print('1')
                    tasks.append((step.to, copy.deepcopy(i)))
                    # print(i, " -> ", step.to)
                elif i[step.what][1] <= step.value:
                    # print('2')
                    continue
                else:
                    # print('3')
                    j = copy.deepcopy(i)
                    j[step.what][0] = step.value+1
                    # print(j, " -> ", step.to)
                    tasks.append((step.to, j))
                    i[step.what][1] = step.value  # goes through
                    # print(i, " next step")
            else:
                # print(i, " -> ", step.to)  # todo R can be skipped
                tasks.append((step.to, copy.deepcopy(i)))
        # print("Sending back ", tasks)
        return tasks


class Solution:
    def __init__(self, path: pathlib.Path):
        self.workflows, self.inputs = path.read_text().split('\n\n')[:2]
        self.workflows = [WorkFlow(line) for line in self.workflows.split('\n')]
        self.inputs = [
            [int(t.split('=')[1].split('}')[0]) for t in i.split(',')]  # x, m, a, s
            for i in self.inputs.split('\n')
            ]

    def solve_a(self) -> int:
        start = None
        for wf in self.workflows:
            if wf.name == 'in':
                start = wf
        assert start is not None
        accu = 0
        for i in self.inputs:
            # # print(i)
            wf = start
            while wf is not None:
                result = wf.process(i)
                # # print(result)
                if result == 'A':
                    accu += sum(i)
                    wf = None
                elif result == 'R':
                    wf = None
                else:
                    for wf2 in self.workflows:
                        if wf2.name == result:
                            wf = wf2
        return accu

    def solve_b(self) -> int:
        accu = 0
        i = [[1, 4000], [1, 4000], [1, 4000], [1, 4000]]
        tasks = [('in', i)]
        while tasks:
            p = tasks.pop(0)
            # print("-----------------------------------------")
            if p[0] == 'A':
                prod = 1
                for j in range(4):
                    prod *= (p[1][j][1] - p[1][j][0] + 1)
                # print(p[1], " accepted, adding ", prod)
                accu += prod
            elif p[0] == 'R':
                # print(p[1], " rejected")
                pass
            else:
                wf2 = None
                for wf in self.workflows:
                    if wf.name == p[0]:
                        wf2 = wf
                tasks.extend(wf2.process2(p[1]))
            # print(tasks)
        return accu


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(19_114, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(432_788, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(167_409_079_868_000, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(142863718918201, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

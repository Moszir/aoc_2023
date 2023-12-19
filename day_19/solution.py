import copy
import math
import pathlib
import typing
import unittest


type Point = typing.Tuple[int, int, int, int]
type Interval = typing.List[typing.List[int]]
type Task = typing.Tuple[str, Interval]
type GoodTask = typing.Optional[Task]
type FurtherTask = typing.Optional[Task]
type Tasks = typing.List[Task]


class Condition:
    def __init__(self, s):
        self.less = '<' in s
        self.greater = '>' in s
        neither = not (self.less or self.greater)
        self.value = None if neither else int(s.split(':')[0][2:])
        self.index = None if neither else 'xmas'.index(s[0])
        self.target = s if neither else s.split(':')[1]
        self.process = (
            (lambda p: self.process_less(p)) if self.less else
            (lambda p: self.process_greater(p)) if self.greater else
            (lambda p: self.process_unconditional(p))
        )
        self.process_interval = (
            (lambda i: self.process_interval_less(i)) if self.less else
            (lambda i: self.process_interval_greater(i)) if self.greater else
            (lambda i: self.process_interval_unconditional(i))
        )

    def process_less(self, point: Point) -> typing.Optional[str]:
        return self.target if point[self.index] < self.value else None

    def process_greater(self, point: Point) -> typing.Optional[str]:
        return self.target if point[self.index] > self.value else None

    def process_unconditional(self, _: Point) -> typing.Optional[str]:
        return self.target

    def process_interval_less(self, interval: Interval) -> typing.Tuple[GoodTask, FurtherTask]:
        a, b = interval[self.index]
        if b < self.value:
            return (self.target, interval), None
        elif a >= self.value:
            return None, ('', interval)
        else:
            good_part = copy.deepcopy(interval)
            good_part[self.index][1] = self.value - 1
            interval[self.index][0] = self.value
            return (self.target, good_part), ('', interval)

    def process_interval_greater(self, interval: Interval) -> typing.Tuple[GoodTask, FurtherTask]:
        a, b = interval[self.index]
        if a > self.value:
            return (self.target, interval), None
        elif b <= self.value:
            return None, ('', interval)
        else:
            good_part = copy.deepcopy(interval)
            good_part[self.index][0] = self.value + 1
            interval[self.index][1] = self.value
            return (self.target, good_part), ('', interval)

    def process_interval_unconditional(self, interval: Interval) -> typing.Tuple[GoodTask, FurtherTask]:
        return (self.target, interval), None


class WorkFlow:
    def __init__(self, line):
        self.name = line.split('{')[0]
        self.steps = [Condition(s) for s in line.split('{')[1][:-1].split(',')]

    def process_point(self, point: Point) -> str:
        """ Processes a single input point.

        Note that the workflow is guaranteed to have an unconditional target at its end.
        """
        for step in self.steps:
            result = step.process(point)
            if result is not None:
                return result

    def process_interval(self, interval: Interval) -> Tasks:
        """ Processes an interval of input points.

        Splits the input interval into subintervals, and returns where they go.
        The returned "task list" can contain 'A' and 'R' as destinations that the caller should handle differently
        than real workflow destinations.
        """
        tasks = []

        for step in self.steps:
            good_task, further_task = step.process_interval(interval)
            if good_task is not None:
                tasks.append(good_task)
            if further_task is not None:
                interval = further_task[1]
            else:
                break
        return tasks


class Solution:
    def __init__(self, path: pathlib.Path):
        workflows, inputs = path.read_text().split('\n\n')[:2]
        self.workflows = [WorkFlow(line) for line in workflows.split('\n')]
        self.inputs: typing.List[Point] = [
            tuple(int(t.split('=')[1].split('}')[0]) for t in i.split(','))
            for i in inputs.split('\n')]

    def find_work_flow(self, name: str) -> WorkFlow:
        return next((wf for wf in self.workflows if wf.name == name))

    def process_point(self, point: Point) -> bool:
        wf = self.find_work_flow('in')
        while True:
            result = wf.process_point(point)
            if result == 'A':
                return True
            elif result == 'R':
                return False
            else:
                wf = self.find_work_flow(result)

    def solve_a(self) -> int:
        return sum((sum(point) for point in self.inputs if self.process_point(point)))

    def solve_b(self) -> int:
        accu = 0
        tasks = [('in', [[1, 4000], [1, 4000], [1, 4000], [1, 4000]])]
        while tasks:
            p = tasks.pop(0)
            if p[0] == 'A':
                accu += math.prod((p[1][j][1] - p[1][j][0] + 1 for j in range(4)))
            elif p[0] != 'R':
                tasks.extend(self.find_work_flow(p[0]).process_interval(p[1]))
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
        self.assertEqual(142_863_718_918_201, self.real_input().solve_b())


if __name__ == '__main__':
    unittest.main()

import math
import typing
import unittest

type Point2D[t] = typing.Tuple[t, t]
type Vertices2D[t] = typing.List[Point2D[t]]


def shoe_lace_area[t](vertices: Vertices2D[t]) -> float:
    area = 0
    for v, w in zip(vertices, vertices[1:]):
        area += v[0] * w[1] - v[1] * w[0]
    if vertices[-1] != vertices[0]:  # The user passed a non-closed loop. Pretend that we added v[0] to the end.
        area += vertices[-1][0] * vertices[0][1] - vertices[-1][1] * vertices[0][0]
    return abs(area / 2)


def heron[T](a: T, b: T, c: T) -> float:
    s = (a+b+c) / 2
    return math.sqrt(s * (s-a) * (s-b) * (s-c))


def heron_stable[T](a: T, b: T, c: T) -> float:
    a, b, c = sorted((a, b, c), reverse=True)  # a >= b >= c
    return 0.25 * math.sqrt((a+b+c) * (a+b-c) * (b+c-a) * (c+a-b))


class Tests(unittest.TestCase):
    def test_shoe_lace_area(self):
        # Some collinear polygons
        self.assertEqual(0.0, shoe_lace_area([(2, 3), (3, 4.5), (4, 6), (2, 3)]))
        self.assertEqual(0.0, shoe_lace_area([(2, 3), (3, 4.5), (4, 6)]))

        # Small right triangle
        self.assertEqual(0.5, shoe_lace_area([(2, 0), (2, 1), (3, 0), (2, 0)]))
        self.assertEqual(0.5, shoe_lace_area([(2, 0), (2, 1), (3, 0)]))  # forgot to close the loop

        # Move it further away
        self.assertEqual(0.5, shoe_lace_area([(20, 0), (20, 1), (21, 0), (20, 0)]))
        self.assertEqual(0.5, shoe_lace_area([(20, 0), (20, 1), (21, 0)]))

        # From AoC 2023/19: example input
        p = [(0, 0), (0, 6), (5, 6), (5, 4), (7, 4), (7, 6), (9, 6), (9, 1), (7, 1), (7, 0), (5, 0), (5, 2),
             (2, 2), (2, 0), (0, 0)]
        self.assertEqual(42.0, shoe_lace_area(p))

    def test_heron(self):
        self.assertRaises(ValueError, heron, 0, 2, 3)
        self.assertEqual(0.0, heron(1, 2, 3))
        self.assertEqual(6.0, heron(3, 4, 5))
        self.assertEqual(math.sqrt(3)/4.0, heron(1, 1, 1))
        self.assertEqual(math.sqrt(3), heron(2, 2, 2))

    def test_heron_stable(self):
        self.assertRaises(ValueError, heron_stable, 0, 2, 3)
        self.assertEqual(0.0, heron_stable(3, 1, 2))
        self.assertEqual(6.0, heron_stable(5, 4, 3))
        self.assertEqual(math.sqrt(3)/4.0, heron_stable(1, 1, 1))
        self.assertEqual(math.sqrt(3), heron_stable(2, 2, 2))


if __name__ == '__main__':
    unittest.main()

""" Various maths snippets """
import typing


def min_max[T](a: T, b: T) -> typing.Tuple[T, T]:
    return min(a, b), max(a, b)

import dataclasses
import math
import typing
import unittest


@dataclasses.dataclass
class Node:
    left: str
    right: str


class Solution:

    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            lines = [line.strip() for line in test_input.readlines()]
            self.__instructions = lines[0]
            self.__nodes = {
                line[:3]: Node(line[7:10], line[12:15])
                for line in lines[2:]
            }

    def solve_a(self) -> int:
        position = 'AAA'
        steps = 0
        while position != 'ZZZ':
            instruction = self.__instructions[steps % len(self.__instructions)]
            node = self.__nodes[position]
            if instruction == 'L':
                position = node.left
            else:
                position = node.right
            steps += 1
        return steps

    def solve_b_brute_force(self) -> int:
        positions: typing.List[str] = [key for key in self.__nodes.keys() if key[-1] == 'A']
        steps = 0
        while not all(p[-1] == 'Z' for p in positions):
            i = self.__instructions[steps % len(self.__instructions)]
            positions = [
                self.__nodes[p].left if i == 'L' else self.__nodes[p].right
                for p in positions
            ]
            steps += 1
        return steps

    def check_data(self) -> bool:
        print(f'Directions length = {len(self.__instructions)}')
        starting_positions = [key for key in self.__nodes.keys() if key[-1] == 'A']
        starting_positions_good = []
        for starting_position in starting_positions:
            print(f'Checking {starting_position}')
            position = starting_position
            steps = 0
            hits = []
            positions_hit = []
            while len(hits) != 10:
                while position[-1] != 'Z':
                    direction = self.__instructions[steps % len(self.__instructions)]
                    node = self.__nodes[position]
                    position = node.left if direction == 'L' else node.right
                    steps += 1
                hits.append(steps)
                positions_hit.append(position)
                direction = self.__instructions[steps % len(self.__instructions)]
                node = self.__nodes[position]
                position = node.left if direction == 'L' else node.right
                steps += 1
            print(f'  first 10 Z hits at {hits}')
            print(f'  positions hit: {positions_hit}')
            print(f'  dividing with first element: {[h/hits[0] for h in hits]}')
            print(f'  first element / directions length = {hits[0] / len(self.__instructions)}')
            starting_positions_good.append(
                all(h % hits[0] == 0 for h in hits)
                and hits[0] % len(self.__instructions) == 0)
        print(f'Returning {all(starting_positions_good)}')
        return all(starting_positions_good)

    def solve_b(self) -> int:
        """
        This is NOT a general solution.
        It assumes that each starting position hits an endpoint cyclically,
        i.e. at exactly every nth step for some n.

        In general, a state can be described by (position, steps % instructions).
        This is a finite state machine, therefore for each starting position the evolution of the machine
        consists of a finite starting section, and a cycle.

        A general solution would be
        - Create this representation for each starting position
        - Reduce this representation:
          - starting section indexes (where position ends with a 'Z'): s0, s1, ..., s_max
          - starting section length: S
          - cycle indexes: c0, ..., cy
          - cycle length: C
          - Then the matches in the cycling section look like: `S + n*C + ck` for some non-negative n, and ck.
        - Check the starting sections:
          - Let t_0 < t_1 < ... be the union of the starting sections
          - Check them in ascending order: if for every starting position t_i is either in the starting section indexes,
            or is of the form `S + n*C + ck`, then it is the solution, return.
        - Otherwise, the solution is in the cycle section of all starting positions
          - For every set of (c_1, ..., c_p) where c_j is a cycle index of starting position j:
            - We should find the smallest V, such that it is of the form `S_j + n_j*C_j + c_j`
              for some n_j non-negative, for all j.
            - Then `V = S_j + n_j*C_j + c_j` -> `V === S_j + c_j (mod C_j)` for all j.
            - This can be solved by the Chinese remainder theorem
              - Note that `S_j + c_j === S_k + c_k (mod gcd(C_j, C_k))` must hold for each pair.
              - This is trivial if C_j and C_k are relative primes, which is the basic case of the CRT.
              - If it does not hold, then there is no solution.
                - Example: 2k+1 = L = 4m + 2 will not have a solution.
            - The solution is a congruence class modulo lcm(C_1, ..., C_p)
            - Find the smallest V in the class such that V = S_j + n_j * C_j + c_j for a non-negative n_j for every j.
          - It is possible that neither of the c_i combinations yielded a solution:
            ``` L

                AAA BAA XXX
                BAA ZZZ XXX
                ZZZ AAA XXX
            ```
            Here both ghosts cycle on the AAA -> BAA -> ZZZ -> AAA cycle, one chasing the other.
          - Otherwise, return the smallest V.

        The input in my case (and surely in every generated input) is such that
        each starting position has only one cyclic index, no starting section index, S_j + c_j === 0 (C_j) for all j,
        and so the solution is lcm(C_j).
        """

        positions: typing.List[str] = [key for key in self.__nodes.keys() if key[-1] == 'A']
        cycle_lengths: typing.List[int] = []

        for position in positions:
            steps = 0
            while position[-1] != 'Z':
                instruction = self.__instructions[steps % len(self.__instructions)]
                position = self.__nodes[position].left if instruction == 'L' else self.__nodes[position].right
                steps += 1
            cycle_lengths.append(steps)
        return math.lcm(*cycle_lengths)


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(2, Solution('example.txt').solve_a())

    def test_a_example_2(self):
        self.assertEqual(6, Solution('example_2.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(14_893, Solution('input.txt').solve_a())

    def test_b_example(self):
        solution = Solution('example_b.txt')
        self.assertEqual(6, solution.solve_b())
        self.assertEqual(6, solution.solve_b_brute_force())

    def test_b_input(self):
        solution = Solution('input.txt')
        self.assertTrue(solution.check_data())
        self.assertEqual(10_241_191_004_509, solution.solve_b())

    def test_counter_example(self):
        # Show that `solve_b` is NOT actually correct in general.
        solution = Solution('counter_example.txt')
        self.assertEqual(10, solution.solve_b_brute_force())
        self.assertEqual(3, solution.solve_b())


if __name__ == '__main__':
    unittest.main()

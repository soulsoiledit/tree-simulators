from fractions import Fraction
from typing import override

from lib import Logs, State, safe_inc

from .base import Tree


class Forking(Tree):
    def __init__(self, base: int, first: int, second: int):
        super().__init__(
            [
                [base],
                range(first + 1),
                range(second + 1),
                range(4),
                range(3),
                range(2),
                range(3),
            ]
        )

    @override
    def grow(self, state: State) -> Logs:
        (
            base,
            first,
            second,
            lean_height,
            lean_length,
            branch_height,
            branch_length,
        ) = state
        height = base + first + second
        lean_height = height - lean_height - 1
        lean_length = 3 - lean_length
        branch_y = lean_height - branch_height - 1
        branch_length = 1 + branch_length

        logs: Logs = []
        ring = 0

        for y in range(height):
            if y >= lean_height and lean_length > 0:
                ring += 1
                lean_length -= 1
            safe_inc(logs, ring, Fraction(1))

        ring = 0
        branch_chance = Fraction(3, 4)
        for y in range(branch_y, height):
            if branch_length <= 0:
                break
            if y >= 1:
                ring += 1
                safe_inc(logs, ring, branch_chance)
            branch_length -= 1

        return logs

from fractions import Fraction
from typing import override

from lib import IntCollection, LogAmount, Logs, State, safe_inc

from .base import Tree


class Bending(Tree):
    def __init__(self, base: int, first: int, second: int, bend_length: IntCollection):
        super().__init__(
            [
                [base],
                range(first + 1),
                range(second + 1),
                range(2),
                bend_length,
            ]
        )

    @override
    def grow(self, state: State) -> Logs:
        base, first, second, bend_height, bend_length = state
        height = base + first + second - 1

        logs: list[LogAmount] = []
        ring = 0

        for i in range(height + 1):
            if i + 1 >= height + bend_height:
                ring += 1
            safe_inc(logs, ring, Fraction(1))

        for i in range(bend_length + 1):
            safe_inc(logs, ring, Fraction(1))
            ring += 1

        return logs

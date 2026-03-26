from fractions import Fraction
from typing import override

from lib import Logs, State

from .base import Tree


class RedMushroom(Tree):
    def __init__(self, radius: int) -> None:
        super().__init__(
            [
                [4],
                range(3),
                range(12),
                [radius],
            ]
        )

    @override
    def grow(self, state: State) -> Logs:
        base, first, should_double, radius = state
        logs: Logs = [Fraction(0)] * (radius + 1)

        height = base + first
        if should_double == 0:
            height *= 2
        logs[0] += Fraction(height)

        logs[radius] += Fraction(3 * 4 * (2 * radius - 1))

        for r in range(radius):
            if r == 0:
                logs[0] += Fraction(1)
            else:
                logs[r] += Fraction(8 * r)

        return logs

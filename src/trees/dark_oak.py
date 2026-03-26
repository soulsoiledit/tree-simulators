from fractions import Fraction
from typing import override

from lib import Logs, State, safe_inc

from .base import Tree


class DarkOak(Tree):
    def __init__(self, base: int, first: int, second: int) -> None:
        super().__init__(
            [
                [base],
                range(first + 1),
                range(second + 1),
                range(4),
                range(3),
            ]
        )

    @override
    def grow(self, state: State) -> Logs:
        base, first, second, lean_offset, lean_steps = state
        height = base + first + second
        lean_height = height - lean_offset
        lean_steps = 2 - lean_steps
        branch_start = height - 1

        logs: Logs = []
        ring = 0
        for y in range(height):
            if y >= lean_height and lean_steps > 0:
                ring += 1
                lean_steps -= 1
            safe_inc(logs, max(ring - 1, 0), Fraction(2))
            safe_inc(logs, ring, Fraction(2))

            dist_from_start = branch_start - y
            if not (1 <= dist_from_start <= 4):
                continue

            # lower logs have lower chance to generate
            branch_prob = Fraction(5 - max(2, dist_from_start), 3)
            max_logs = 12 if ring == 0 else 10
            # 1/3 chance for each log to generate
            safe_inc(logs, 1, Fraction(max_logs, 3) * branch_prob)

        return logs

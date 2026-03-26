from fractions import Fraction
from typing import override

from lib import Logs, State

from .base import Tree


class Giant(Tree):
    def __init__(self, base: int, first: int, second: int) -> None:
        super().__init__(
            [
                [base],
                range(first + 1),
                range(second + 1),
            ]
        )

    @override
    def grow(self, state: State) -> Logs:
        height = sum(state)
        return [Fraction(height * 4 - 3)]

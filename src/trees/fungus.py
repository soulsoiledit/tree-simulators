from fractions import Fraction
from typing import override

from lib import Logs, State

from .base import Tree


class Fungus(Tree):
    def __init__(self) -> None:
        super().__init__(
            [
                range(4, 14),
                range(12),
            ]
        )

    @override
    def grow(self, state: State) -> Logs:
        height = state[0]
        should_double = state[1]
        if should_double == 0:
            height *= 2
        return [Fraction(height)]

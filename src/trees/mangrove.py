from fractions import Fraction
from itertools import product, zip_longest
from typing import override

from lib import IntCollection, Logs, State, safe_inc

from .base import Tree


class MangroveVariant(Tree):
    def __init__(
        self,
        base: int,
        first: int,
        second: int,
        branch_steps: IntCollection,
        branch_prob: float,
        branch_extra_steps: IntCollection,
    ) -> None:
        super().__init__(
            [
                [base],
                range(first + 1),
                range(second + 1),
            ]
        )
        self.branch_steps = branch_steps
        self.branch_prob = Fraction(str(branch_prob))
        self.branch_offset = branch_extra_steps

    @override
    def grow(self, state: State) -> Logs:
        base, first, second = state
        height = base + first + second

        logs: Logs = [Fraction(height)]

        branch_logs: Logs = [Fraction()]
        num_branch_steps = len(self.branch_steps)
        num_branch_offset = len(self.branch_offset)
        branch_weight = Fraction(1, num_branch_steps * num_branch_offset**2)
        for steps, offset1, offset2 in product(
            self.branch_steps, self.branch_offset, self.branch_offset
        ):
            ring = max(0, offset1 - offset2 - 1)
            current_steps = steps
            while ring < height and current_steps > 0:
                if ring >= 1:
                    safe_inc(branch_logs, ring, branch_weight)
                ring += 1
                current_steps -= 1

        expected_branches = (height - 1) * self.branch_prob
        for ring, blocks in enumerate(branch_logs):
            safe_inc(logs, ring, blocks * expected_branches)

        return logs


class Mangrove(Tree):
    def __init__(
        self, alt_prob: float, main: MangroveVariant, alt: MangroveVariant
    ) -> None:
        super().__init__([[0]])
        self.alt_prob = Fraction(str(alt_prob))
        self.main = main
        self.alt = alt

    @override
    def grow(self, state: State) -> Logs:
        from analyzer import Results

        main_results = Results(self.main)
        alt_results = Results(self.alt)

        print(f"-- Short Mangrove: {main_results}")
        print(f"-- Tall Mangrove: {alt_results}")

        return [
            alt_val * self.alt_prob + main_val * (1 - self.alt_prob)
            for main_val, alt_val in zip_longest(
                main_results.averages, alt_results.averages, fillvalue=Fraction(0)
            )
        ]

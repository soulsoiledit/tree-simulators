import math
from fractions import Fraction
from itertools import product, zip_longest
from typing import override

from lib import Logs, format_list
from trees import Tree


class Results:
    def __init__(self, tree: Tree):
        log_map = {state: tree.grow(state) for state in product(*tree.states)}

        self.totals, scale = self.scale_fractional_total(
            [sum(col) for col in list(zip_longest(*log_map.values(), fillvalue=0))]
        )
        self.unique: int = len(log_map) * scale
        self.averages: Logs = [total / self.unique for total in self.totals]

    def scale_fractional_total(self, logs: Logs) -> tuple[Logs, int]:
        denoms = [f.denominator for f in logs if isinstance(f, Fraction)]
        if not denoms:
            return logs, 1

        lcm = math.lcm(*denoms)
        return [lcm * f for f in logs], lcm

    @override
    def __str__(self):
        return f"{self.unique} {format_list(self.totals)} {format_list(self.averages)}"

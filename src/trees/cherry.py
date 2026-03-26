from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product
from typing import override

from lib import IntCollection, Logs, State, safe_inc

from .base import Tree

type XYProbGrid = dict[tuple[int, int], Fraction]


class Cherry(Tree):
    def __init__(
        self,
        base: int,
        a: int,
        b: int,
        branch_count: IntCollection,
        branch_length: IntCollection,
        branch_start_offset: range,
        branch_end_offset: IntCollection,
    ) -> None:
        super().__init__([[base], range(a + 1), range(b + 1), branch_count])
        self.branch_count = branch_count
        self.branch_length = branch_length
        self.branch_start_offset = branch_start_offset
        self.branch_end_offset = branch_end_offset

    @lru_cache(1024)
    def generate_branch(
        self,
        tree_height: int,
        branch_height: int,
        has_extended_trunk: bool,
        branch_length: int,
        branch_end_offset: int,
    ) -> tuple[Fraction, ...]:
        logs = [Fraction(0)]

        end_height = tree_height - 1 + branch_end_offset
        extended = has_extended_trunk or (end_height < branch_height)
        end_distance = branch_length + (1 if extended else 0)
        steps_x = 2 if extended else 1

        cur_x, cur_y = 0, branch_height
        goal_x, goal_y = end_distance, end_height
        vertical_dir = 1 if goal_y > cur_y else -1

        for _ in range(steps_x):
            cur_x += 1
            safe_inc(logs, cur_x, Fraction(1))

        # build probability grid of remaining log positions
        prob_grid: XYProbGrid = {(cur_x, cur_y): Fraction(1)}

        while prob_grid:
            next_grid: XYProbGrid = defaultdict(Fraction)
            for (x, y), prob in prob_grid.items():
                if x == goal_x and y == goal_y:
                    continue

                dx = goal_x - x
                dy = abs(goal_y - y)
                mhtn_dist = dx + dy

                prob_y = Fraction(dy, mhtn_dist)
                prob_x = 1 - prob_y

                if dy > 0:
                    next_prob = prob * prob_y
                    next_grid[(x, y + vertical_dir)] += next_prob
                    safe_inc(logs, x, next_prob)

                if dx > 0:
                    next_prob = prob * prob_x
                    next_grid[x + 1, y] += next_prob
                    safe_inc(logs, x + 1, next_prob)

            prob_grid = next_grid

        return tuple(logs)

    @override
    def grow(self, state: State) -> Logs:
        logs: Logs = [Fraction()]

        base, a, b, branch_count = state
        tree_height = base + a + b

        branch_start_offset = self.branch_start_offset
        snd_branch_start_offset = range(
            self.branch_start_offset.start, self.branch_start_offset.stop - 1
        )

        # perform all branch permutations at once
        permutations = product(
            branch_start_offset,
            self.branch_length,
            self.branch_end_offset,
            snd_branch_start_offset,
            self.branch_length,
            self.branch_end_offset,
        )
        len_permutations = (
            len(branch_start_offset)
            * len(snd_branch_start_offset)
            * len(self.branch_length) ** 2
            * len(self.branch_end_offset) ** 2
        )
        permutation_weight = Fraction(1, len_permutations)

        for (
            fst_start_offset,
            fst_length,
            fst_end_offset,
            snd_start_offset,
            snd_length,
            snd_end_offset,
        ) in permutations:
            fst_height = max(0, tree_height - 1 + fst_start_offset)
            snd_height = max(0, tree_height - 1 + snd_start_offset)
            if snd_height >= fst_height:
                snd_height += 1

            has_middle = branch_count == 3
            has_two = branch_count >= 2

            trunk_height: int
            if has_middle:
                trunk_height = tree_height
            elif has_two:
                trunk_height = max(fst_height, snd_height) + 1
            else:
                trunk_height = fst_height + 1

            safe_inc(logs, 0, Fraction(trunk_height) * permutation_weight)

            f_logs = self.generate_branch(
                tree_height,
                fst_height,
                fst_height < (trunk_height - 1),
                fst_length,
                fst_end_offset,
            )
            for ring, blocks in enumerate(f_logs):
                safe_inc(logs, ring, blocks * permutation_weight)

            if has_two:
                s_logs = self.generate_branch(
                    tree_height,
                    snd_height,
                    snd_height < (trunk_height - 1),
                    snd_length,
                    snd_end_offset,
                )
                for ring, blocks in enumerate(s_logs):
                    safe_inc(logs, ring, blocks * permutation_weight)

        return logs

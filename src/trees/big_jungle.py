import math
from itertools import pairwise
from typing import Final, override

from lib import Logs, State, safe_inc

from .giant import Giant

HALF_PI: Final[float] = math.pi / 2
TAU: Final[float] = math.tau


class BigJungle(Giant):
    def __init__(self, base: int, first: int, second: int):
        super().__init__(base, first, second)
        self.states.extend([range(4)])
        self.ring_weights = self.get_ring_weights()

    def get_ring_weights(self) -> list[float]:
        critical_angles = {0.0, TAU}
        for b in range(5):
            # r = int(1.5 + cos/sin(theta) * b )
            min_r = math.ceil(1.5 - b)
            max_r = math.floor(1.5 + b)
            for r in range(min_r, max_r + 1):
                # theta = acos/asin((r - 1.5) / b)
                ratio = (r - 1.5) / b
                theta_cos = math.acos(ratio)
                theta_sin = math.asin(ratio)
                for quad in range(4):
                    shift = quad * HALF_PI
                    critical_angles.add((theta_cos + shift) % TAU)
                    critical_angles.add((theta_sin + shift) % TAU)

        ring_weights = [0.0]
        sorted_angles = sorted(critical_angles)
        for prev_angle, next_angle in pairwise(sorted_angles):
            delta_angle = next_angle - prev_angle
            midpoint = (next_angle + prev_angle) / 2
            for b in range(5):
                bx = int(1.5 + math.cos(midpoint) * b)
                bz = int(1.5 + math.sin(midpoint) * b)
                # 2x2 center from 0,0 to 1,1, so positive outer coords are stepped down
                rx = 0 if (0 <= bx <= 1) else abs(bx) if bx < 0 else bx - 1
                rz = 0 if (0 <= bz <= 1) else abs(bz) if bz < 0 else bz - 1
                ring = max(rx, rz)
                if ring > 0:
                    safe_inc(ring_weights, ring, delta_angle / TAU)

        return ring_weights

    @override
    def grow(self, state: State) -> Logs:
        base, first, second, branch_offset = state
        height = base + first + second
        branch_height = height - 2 - branch_offset
        half_height = height // 2
        branch_span = branch_height - half_height

        logs: Logs = super().grow((base, first, second))
        if branch_span <= 0:
            return logs

        # step down branch span to find expected branch count
        expected_branches = 0.0
        branch_weights = [0.0] * (branch_span + 1)
        branch_weights[branch_span] = 1.0
        for y in range(branch_span, 0, -1):
            bw = branch_weights[y]
            if bw <= 0.0:
                continue
            expected_branches += bw
            w_quarter = bw / 4
            for i in range(4):
                new_y = y - 2 - i
                if new_y > 0:
                    branch_weights[new_y] += w_quarter

        for ring, rw in enumerate(self.ring_weights):
            safe_inc(logs, ring, expected_branches * rw)

        return logs

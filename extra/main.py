from typing import overload
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

type States = list[int]
type State = tuple[int, ...]
type Shape = list[Fraction]
type ShapeMap = dict[State, Shape]


@dataclass
class Statistics:
    unique: int
    sums: list[Fraction]
    averages: list[Fraction]


def irange(a, b=None) -> range:
    if b:
        return range(a, b + 1)
    return range(a + 1)


def format_list_fractions(fractions: list[Fraction]) -> str:
    return "[{}]".format(", ".join([f"{f}" for f in fractions]))


class Tree:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.states: list[range] = []

    def grow(self, state: State) -> Shape:
        return

    def get_shapes(self) -> ShapeMap:
        shapes: ShapeMap = {}
        for state in product(*self.states):
            shapes[state] = self.grow(state)
        return shapes

    def get_statistics(self) -> Statistics:
        shapes: ShapeMap = self.get_shapes()

        items = shapes.items()
        shape_length = max(map(lambda x: len(x[1]), iter(items)))
        num_shapes = len(items)

        sums = [Fraction(0)] * shape_length
        averages = [Fraction(0)] * shape_length

        for _, shape in items:
            for i, blocks in enumerate(shape):
                sums[i] += blocks

        for i, sum in enumerate(sums):
            averages[i] = sum / num_shapes

        return Statistics(num_shapes, sums, averages)

    def print_results(self) -> None:
        statistics = self.get_statistics()
        sums_formatted = format_list_fractions(statistics.sums)
        averages_formatted = format_list_fractions(statistics.averages)
        print(
            "{}: {} {} {}".format(
                self.name, statistics.unique, sums_formatted, averages_formatted
            )
        )


class Straight(Tree):
    def __init__(
        self, name: str, base_height: int, first_random: int, second_random: int
    ) -> None:
        self.name = name
        self.base_height = base_height
        self.states = [irange(first_random), irange(second_random)]

    def grow(self, state: State) -> Shape:
        first_height = state[0]
        second_height = state[1]
        return [Fraction(self.base_height + first_height + second_height)]


class Giant(Tree):
    def __init__(
        self, name: str, base_height: int, first_random: int, second_random: int
    ) -> None:
        self.name = name
        self.base_height = base_height
        self.states = [irange(first_random), irange(second_random)]

    def grow(self, state: State) -> Shape:
        first_height = state[0]
        second_height = state[1]
        height = self.base_height + first_height + second_height
        logs = height * 4 - 3
        return [Fraction(logs)]


class HugeFungus(Tree):
    def __init__(self, name: str) -> None:
        self.name = name
        self.states = [irange(4, 13), range(12)]

    def grow(self, state: State) -> Shape:
        height = state[0]
        should_double = state[1]
        if should_double == 0:
            height *= 2
        return [Fraction(height)]


class HugeMushroom(Tree):
    CAP: int = 45

    def __init__(self, name: str) -> None:
        self.name = name
        self.states = [irange(4, 6), range(12)]

    def grow(self, state: State) -> Shape:
        height = state[0]
        should_double = state[1]
        if should_double == 0:
            height *= 2
        return [Fraction(height), Fraction(45)]


class Forking(Tree):
    def __init__(
        self, name: str, base_height: int, first_random: int, second_random: int
    ) -> None:
        self.name = name
        self.base_height = base_height
        self.states = [
            irange(first_random),
            irange(second_random),
            range(4),
            irange(1, 3),
            range(4),
            range(2),
            irange(1, 3),
        ]

    def grow(self, state: State) -> Shape:
        (
            first_height,
            second_height,
            first_branch_offset,
            first_branch_length,
            make_second_branch,
            second_branch_offset,
            second_branch_length,
        ) = state

        height = self.base_height + first_height + second_height

        logs = [Fraction(0)] * 4
        offset = 0

        base_trunk_height = height - first_branch_offset - 1

        for n in range(height):
            if n >= base_trunk_height and first_branch_length > 0:
                offset += 1
                first_branch_length -= 1
            logs[offset] += 1

        offset = 0
        remaining_trunk_height = base_trunk_height - second_branch_offset - 1

        if make_second_branch:
            for q in range(remaining_trunk_height, height):
                if second_branch_length <= 0:
                    break
                if q >= 1:
                    offset += 1
                    logs[offset] += 1
                second_branch_length -= 1

        return logs


class Bending(Tree):
    def __init__(
        self,
        name: str,
        base_height: int,
        first_random: int,
        second_random: int,
        leaf_height: int,
        bend_length: tuple[int, int],
    ) -> None:
        self.name = name
        self.base_height = base_height
        self.states = [
            irange(first_random),
            irange(second_random),
            range(2),
            irange(*bend_length),
        ]

    def grow(self, state: State) -> Shape:
        first_height, second_height, branch_height, bend_length = state
        height = self.base_height + first_height + second_height

        logs = [Fraction(0)]
        offset = 0

        for k in range(height):
            if k + 2 >= height + branch_height:
                offset += 1
                logs.append(Fraction(0))
            logs[offset] += 1

        for k in range(bend_length + 1):
            logs[offset] += 1
            offset += 1
            if k < bend_length:
                logs.append(Fraction(0))

        return logs


class DarkOak(Tree):
    def __init__(
        self, name: str, base_height: int, first_random: int, second_random: int
    ) -> None:
        self.name = name
        self.base_height = base_height
        self.states = [
            irange(first_random),
            irange(second_random),
            range(4),
            range(3),
        ]

    def grow(self, state: State) -> Shape:
        first_height, second_height, branch_offset, branch_length = state
        height = self.base_height + first_height + second_height

        logs = [Fraction(0)] * 3
        offset = 0

        branch_min_height = height - branch_offset
        branch_length_ = 2 - branch_length

        for x in range(height):
            if x >= branch_min_height and branch_length_ > 0:
                offset += 1
                branch_length_ -= 1
            logs[offset] += 2
            logs[max(0, offset - 1)] += 2

        # Code runs 1/9 of the time in real world
        branch_max_height = height - 1
        for large_trunk_boost in range(3):
            large_trunk_height = 2 + large_trunk_boost
            for x in range(large_trunk_height):
                # Logs in this range have already been placed
                y_pos = branch_max_height - x - 1
                if branch_min_height <= y_pos <= branch_max_height and offset:
                    logs[1] += Fraction(10, 9)
                else:
                    logs[1] += Fraction(12, 9)

        return logs


# def giant_jungle(base, first, second):
#     table = {}
#
#     # generate multipliers for each branch
#     asin_1_4 = math.asin(1 / 4)
#     asin_3_4 = math.asin(3 / 4)
#     asin_1_2 = math.pi / 6
#     asin_5_6 = math.asin(5 / 6)
#     asin_5_8 = math.asin(5 / 8)
#     asin_7_8 = math.asin(7 / 8)
#     branch_mult = [
#         0,
#         (7 / 12) + (asin_7_8 + asin_1_2 - asin_5_6 + 2 * asin_3_4 - asin_1_4) / math.pi,
#         1.25 + (asin_5_8 - asin_7_8 + 2 * asin_5_6 - asin_1_2 - 2 * asin_3_4) / math.pi,
#         0.75 + (2 * asin_7_8 - asin_5_8 - 2 * asin_5_6) / math.pi,
#         1 - (2 * asin_7_8) / math.pi,
#     ]
#
#     config = product(range(first + 1), range(second + 1), range(3 + 1))
#     for first, second, trunk_sub in config:
#         logs = [0] * 5
#
#         height = base + first + second
#         logs[0] += 4 * height - 3
#
#         branch_height = height - 2 - trunk_sub
#         max_iter = math.floor(height / 4)
#         sequences = product(range(4), repeat=max_iter)
#
#         temp = 0
#         for seq in sequences:
#             temp_branch = branch_height
#             for step in seq:
#                 if not (temp_branch > height / 2):
#                     break
#                 temp += 1
#                 temp_branch -= 2 + step
#         temp_scaled = temp / (4**max_iter)
#
#         for index in range(len(logs)):
#             logs[index] += temp_scaled * branch_mult[index]
#
#         key = (first, second, trunk_sub)
#         table[key] = logs
#
#     return table
#
#
# def mangrove(base, first, second, branch_len, branch_chance):
#     table = {}
#
#     max_branch_len = max(branch_len) - min(branch_len) + 1
#
#     config = product(range(first + 1), range(second + 1))
#
#     for first, second in config:
#         logs = [0] * max_branch_len
#         height = base + first + second
#
#         # find average logs per branch
#         branch_logs = logs.copy()
#         for l_ in range(branch_len[0], branch_len[1] + 1):
#             offset = 0
#             remaining_len = l_ - 1
#
#             for _ in range(1, height):
#                 if not remaining_len > 0:
#                     break
#                 offset += 1
#                 branch_logs[offset] += branch_chance
#                 remaining_len -= 1
#
#         logs[0] += height
#         for index in range(len(logs)):
#             branch_logs[index] /= max_branch_len
#             branch_logs[index] *= height - 1
#             logs[index] += branch_logs[index]
#
#         key = (first, second)
#         table[key] = logs
#
#     return table
#
#
# def cherry(base, first, second, branch_count, branch_len, branch_start, branch_end):
#     def generate_branch(height, start, low, length, end):
#         logs = [0] * 6
#         offset = 0
#
#         end = height - 1 + end
#         long = low or (end < start)
#         end_len = length + (1 if long else 0)
#         base_len = 2 if long else 1
#
#         # go out by the starting length
#         for _ in range(base_len):
#             offset += 1
#             logs[offset] += 1
#
#         # create probability tree
#         manhattan = (end + end_len) - base_len - start
#         sequences = product((False, True), repeat=manhattan)
#
#         # iterate over all possible branch generations
#         for seq in sequences:
#             temp_manhattan = manhattan
#             remaining_height = end
#             remaining_len = end_len - base_len
#             temp_offset = offset
#             temp_logs = [0] * 6
#             chance = 1
#
#             for go_up in seq:
#                 y_error = abs(remaining_height - start) / temp_manhattan
#
#                 if go_up:
#                     # multiply chance by probability of this event occuring
#                     chance *= y_error
#                     # not all combinations are valid
#                     if remaining_height > 0:
#                         remaining_height -= 1
#                 else:
#                     chance *= 1 - y_error
#                     if remaining_len > 0:
#                         remaining_len -= 1
#                         temp_offset += 1
#
#                 temp_logs[temp_offset] += 1
#                 temp_manhattan -= 1
#
#             # add logs generated divided by chance of branch occuring
#             for index in range(len(temp_logs)):
#                 logs[index] += temp_logs[index] * chance
#
#         return logs
#
#     table = {}
#
#     br_length = range(branch_len[0], branch_len[1] + 1)
#     f_br_offset = range(branch_start[0], branch_start[1] + 1)
#     s_br_offset = range(branch_start[0], branch_start[1])
#     end_offset = range(branch_end[0], branch_end[1] + 1)
#
#     config = product(
#         range(first + 1),
#         range(second + 1),
#         branch_count,
#         f_br_offset,
#         br_length,
#         end_offset,
#         s_br_offset,
#         br_length,
#         end_offset,
#     )
#     for first, second, count, f_offset, f_len, f_end, s_offset, s_len, s_end in config:
#         logs = [0] * 6
#
#         height = base + first + second
#         fb_height = height - 1 + f_offset
#         sb_height = height - 1 + s_offset
#         if sb_height >= fb_height:
#             sb_height += 1
#
#         trunk = (
#             fb_height + 1
#             if count < 2
#             else height
#             if count == 3
#             else max(fb_height, sb_height) + 1
#         )
#         logs[0] += trunk
#
#         f_branch = generate_branch(
#             height, fb_height, fb_height < (trunk - 1), f_len, f_end
#         )
#         for index in range(len(logs)):
#             logs[index] += f_branch[index]
#
#         if count >= 2:
#             s_branch = generate_branch(
#                 height, sb_height, sb_height < (trunk - 1), s_len, s_end
#             )
#             for index in range(len(logs)):
#                 logs[index] += s_branch[index]
#
#         key = (first, second, count, f_offset, f_len, f_end, s_offset, s_len, s_end)
#         table[key] = logs
#
#     return table


def main():
    trees: list[Tree] = [
        Straight("Oak", 4, 2, 0),
        Straight("Birch", 5, 2, 0),
        Straight("Spruce", 5, 2, 1),
        Straight("Jungle", 4, 8, 0),
        #
        Forking("Acacia", 5, 2, 2),
        # print_average("Azalea", azalea(4, 2, 0, (1, 2)))
        Bending("Azalea", 4, 2, 0, 3, (1, 2)),
        # print_average("Cherry", cherry(7, 1, 0, (1, 2, 3), (2, 4), (-4, -3), (-1, 0)))
        #
        HugeFungus("Huge Fungus"),
        HugeMushroom("Huge Mushroom"),
        #
        Giant("2x2 Spruce", 13, 2, 14),
        # print_average("Dark Oak", dark_oak(6, 2, 1))
        DarkOak("Dark Oak", 6, 2, 1),
        # print_average("Pale Oak", dark_oak(6, 2, 1))
        # print_average("2x2 Jungle", giant_jungle(10, 2, 19))
        #
        # print_average("Mangrove", mangrove(2, 1, 4, (1, 4), 0.5))
        # print_average("Tall Mangrove", mangrove(4, 1, 9, (1, 6), 0.5))
    ]

    for tree in trees:
        tree.print_results()


if __name__ == "__main__":
    main()

# giant
# fancy
# cherry
# bending
# darkoak
# forking
# straight
# megajungle
# upwardsbranching
# hugeredmushroom
# hugebrownmushroom
# hugebrownmushroom
# hugefungus

from itertools import product, repeat
import math


def simple_generate(base, first, second):
    table = {}

    config = product(range(first + 1), range(second + 1))
    for first, second in config:
        key = (first, second)
        table[key] = [base + first + second]

    return table


def acacia_generate(base, first, second):
    table = {}

    first = range(first + 1)
    second = range(second + 1)
    first_branch_height = range(1, 4 + 1)
    first_branch_length = range(1, 3 + 1)
    second_branch_height = range(1, 2 + 1)
    second_branch_length = range(1, 3 + 1)
    config = product(
        first,
        second,
        first_branch_height,
        first_branch_length,
        second_branch_height,
        second_branch_length,
    )

    for first, second, f_br_height, f_br_length, s_br_height, s_br_length in config:
        logs = [0] * 4
        length = f_br_length
        offset = 0

        height = base + first + second
        trunk_height = height - f_br_height

        for m in range(height):
            if m >= trunk_height and length > 0:
                offset += 1
                length -= 1
            logs[offset] += 1

        offset = 0
        length = s_br_length
        ext_trunk_height = trunk_height - s_br_height

        for p in range(ext_trunk_height, height):
            if not length > 0:
                break
            if p >= 1:
                offset += 1
                # runs only 3/4 of the time
                logs[offset] += 0.75
            length -= 1

        key = (first, second, f_br_height, f_br_length, s_br_height, s_br_length)
        table[key] = logs

    return table


def azalea_generate(base, first, second, bend):
    table = {}

    config = product(
        range(first + 1), range(second + 1), range(2), range(bend[0], bend[1] + 1)
    )
    for first, second, branch_height, bend in config:
        logs = [0] * 5
        offset = 0
        height = base + first + second
        max_height = height - 1

        for d in range(max_height + 1):
            if d + 1 >= max_height + branch_height:
                offset += 1
            logs[offset] += 1

        for _ in range(bend + 1):
            logs[offset] += 1
            offset += 1

        key = (first, second, branch_height, bend)
        table[key] = logs

    return table


def fungus_generate():
    table = {}

    config = product(range(4, 14), range(0, 12))
    for stems, doubled in config:
        trunk = stems if doubled else stems * 2
        key = (stems, doubled)
        table[key] = [trunk]

    return table


def mushroom_generate():
    table = {}

    config = product(range(4, 7), range(0, 12))
    for stems, doubled in config:
        trunk = stems if doubled else stems * 2
        key = (stems, doubled)
        table[key] = [trunk, 45]

    return table


def giant_generate(base, first, second):
    table = {}

    config = product(range(first + 1), range(second + 1))
    for first, second in config:
        key = (first, second)
        table[key] = [(base + first + second) * 4 - 3]

    return table


def giant_jungle_generate(base, first, second):
    table = {}

    # generate multipliers for each branch
    asin_1_4 = math.asin(1 / 4)
    asin_3_4 = math.asin(3 / 4)
    asin_1_2 = math.pi / 6
    asin_5_6 = math.asin(5 / 6)
    asin_5_8 = math.asin(5 / 8)
    asin_7_8 = math.asin(7 / 8)
    branch_mult = [
        0,
        (7 / 12) + (asin_7_8 + asin_1_2 - asin_5_6 + 2 * asin_3_4 - asin_1_4) / math.pi,
        1.25 + (asin_5_8 - asin_7_8 + 2 * asin_5_6 - asin_1_2 - 2 * asin_3_4) / math.pi,
        0.75 + (2 * asin_7_8 - asin_5_8 - 2 * asin_5_6) / math.pi,
        1 - (2 * asin_7_8) / math.pi,
    ]

    config = product(range(first + 1), range(second + 1), range(3 + 1))
    for first, second, trunk_sub in config:
        logs = [0] * 5

        height = base + first + second
        logs[0] += 4 * height - 3

        branch_height = height - 2 - trunk_sub
        max_iter = math.floor(height / 4)
        sequences = product(range(4), repeat=max_iter)

        temp = 0
        for seq in sequences:
            temp_branch = branch_height
            for step in seq:
                if not (temp_branch > height / 2):
                    break
                temp += 1
                temp_branch -= 2 + step
        temp_scaled = temp / (4**max_iter)

        for index in range(len(logs)):
            logs[index] += temp_scaled * branch_mult[index]

        key = (first, second, trunk_sub)
        table[key] = logs

    return table


def dark_oak(base, first, second):
    table = {}

    config = product(range(first + 1), range(second + 1), range(0, 4), range(0, 3))
    for first, second, top_offset, length in config:
        logs = [0] * 3

        height = base + first + second
        branch_height = height - top_offset
        branch_len = 2 - length
        offset = 0

        overlap = []
        for pos in range(height):
            if pos >= branch_height and branch_len > 0:
                offset += 1
                branch_len -= 1
            # append heights where logs could overlap
            match offset:
                case 0:
                    logs[0] += 4
                case 1:
                    logs[0] += 2
                    logs[1] += 2
                    overlap.append(pos)
                case 2:
                    logs[1] += 2
                    logs[2] += 2
                    overlap.append(pos)

        extra_logs = 0
        for rand in range(3):
            s = 2 + rand
            for t in range(s):
                temp_height = height - t - 2
                # add by smaller number when logs could overlap
                if temp_height in overlap:
                    extra_logs += 10
                else:
                    extra_logs += 12
        # divide by 9 since it only runs some of the time
        logs[1] += extra_logs / 9

        key = (first, second, top_offset, length)
        table[key] = logs

    return table


def mangrove_generate(base, first, second, branch_len, branch_chance):
    table = {}

    max_branch_len = max(branch_len) - min(branch_len) + 1

    config = product(range(first + 1), range(second + 1))

    for first, second in config:
        logs = [0] * max_branch_len
        height = base + first + second

        # find average logs per branch
        branch_logs = logs.copy()
        for l in range(branch_len[0], branch_len[1] + 1):
            offset = 0
            remaining_len = l - 1

            for _ in range(1, height):
                if not remaining_len > 0:
                    break
                offset += 1
                branch_logs[offset] += branch_chance
                remaining_len -= 1

        logs[0] += height
        for index in range(len(logs)):
            branch_logs[index] /= max_branch_len
            branch_logs[index] *= height - 1
            logs[index] += branch_logs[index]

        key = (first, second)
        table[key] = logs

    return table


def cherry_generate(
    base, first, second, branch_count, branch_len, branch_start, branch_end
):
    def generate_branch(height, start, low, length, end):
        logs = [0] * 6
        offset = 0

        end = height - 1 + end
        long = low or (end < start)
        end_len = length + (1 if long else 0)
        base_len = 2 if long else 1

        # go out by the starting length
        for _ in range(base_len):
            offset += 1
            logs[offset] += 1

        # create probability tree
        manhattan = (end + end_len) - base_len - start
        sequences = product((False, True), repeat=manhattan)

        # iterate over all possible branch generations
        for seq in sequences:
            temp_manhattan = manhattan
            remaining_height = end
            remaining_len = end_len - base_len
            temp_offset = offset
            temp_logs = [0] * 6
            chance = 1

            for go_up in seq:
                y_error = abs(remaining_height - start) / temp_manhattan

                if go_up:
                    # multiply chance by probability of this event occuring
                    chance *= y_error
                    # not all combinations are valid
                    if remaining_height > 0:
                        remaining_height -= 1
                else:
                    chance *= 1 - y_error
                    if remaining_len > 0:
                        remaining_len -= 1
                        temp_offset += 1

                temp_logs[temp_offset] += 1
                temp_manhattan -= 1

            # add logs generated divided by chance of branch occuring
            for index in range(len(temp_logs)):
                logs[index] += temp_logs[index] * chance

        return logs

    table = {}

    br_length = range(branch_len[0], branch_len[1] + 1)
    f_br_offset = range(branch_start[0], branch_start[1] + 1)
    s_br_offset = range(branch_start[0], branch_start[1])
    end_offset = range(branch_end[0], branch_end[1] + 1)

    config = product(
        range(first + 1),
        range(second + 1),
        branch_count,
        f_br_offset,
        br_length,
        end_offset,
        s_br_offset,
        br_length,
        end_offset,
    )
    for first, second, count, f_offset, f_len, f_end, s_offset, s_len, s_end in config:
        logs = [0] * 6

        height = base + first + second
        fb_height = height - 1 + f_offset
        sb_height = height - 1 + s_offset
        if sb_height >= fb_height:
            sb_height += 1

        trunk = (
            fb_height + 1
            if count < 2
            else height
            if count == 3
            else max(fb_height, sb_height) + 1
        )
        logs[0] += trunk

        f_branch = generate_branch(
            height, fb_height, fb_height < (trunk - 1), f_len, f_end
        )
        for index in range(len(logs)):
            logs[index] += f_branch[index]

        if count >= 2:
            s_branch = generate_branch(
                height, sb_height, sb_height < (trunk - 1), s_len, s_end
            )
            for index in range(len(logs)):
                logs[index] += s_branch[index]

        key = (first, second, count, f_offset, f_len, f_end, s_offset, s_len, s_end)
        table[key] = logs

    return table


def print_average(name, table):
    table_length = len(table.keys())
    value_length = len(list(table.values())[0])
    sums = [0] * value_length

    for value in table.values():
        for index in range(value_length):
            sums[index] += value[index]

    averages = sums.copy()
    for index in range(len(averages)):
        averages[index] /= table_length

    print(f"{name}: {table_length} {sums} {averages}")


def main():
    print_average("Birch", simple_generate(5, 2, 0))
    print_average("Oak", simple_generate(4, 2, 0))
    print_average("Jungle", simple_generate(4, 8, 0))
    print_average("Spruce", simple_generate(5, 2, 1))

    print_average("Acacia", acacia_generate(5, 2, 2))
    print_average("Azalea", azalea_generate(4, 2, 0, (1, 2)))
    print_average(
        "Cherry", cherry_generate(7, 1, 0, (1, 2, 3), (2, 4), (-4, -3), (-1, 0))
    )

    print_average("Fungus", fungus_generate())
    print_average("Mushroom", mushroom_generate())

    print_average("2x2 Spruce", giant_generate(13, 2, 14))
    print_average("Dark Oak", dark_oak(6, 2, 1))
    print_average("2x2 Jungle", giant_jungle_generate(10, 2, 19))

    print_average("Mangrove", mangrove_generate(2, 1, 4, (1, 4), 0.5))
    print_average("Tall Mangrove", mangrove_generate(4, 1, 9, (1, 6), 0.5))

    print_average("Pine", simple_generate(6, 4, 0))
    print_average("2x2 Pine", giant_generate(13, 2, 14))
    print_average("Tall Birch", simple_generate(5, 2, 6))
    print_average("Swamp Oak", simple_generate(5, 3, 0))
    print_average("Jungle Bush", simple_generate(1, 0, 0))


if __name__ == "__main__":
    main()

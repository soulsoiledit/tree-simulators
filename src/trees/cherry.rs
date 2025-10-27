use itertools::{iproduct, repeat_n, Itertools};

use crate::ConfigurationMap;

use fraction::Fraction;

type F = Fraction;

// TODO:
fn generate_branch(
    tree_height: i32,
    start_height: i32,
    is_low_branch: bool,
    length: i32,
    end_offset: i32,
) -> Vec<Fraction> {
    let mut branch_logs = vec![F::from(0); 6];
    let mut branch_offset = 0;

    let end_height = tree_height - 1 + end_offset;
    let long_branch = is_low_branch || (end_height < start_height);
    let end_length = length + if long_branch { 1 } else { 0 };
    let base_length = if long_branch { 2 } else { 1 };

    // Go outwards by the starting lenght
    for _ in 0..base_length {
        branch_offset += 1;
        branch_logs[branch_offset] += 1;
    }

    // Create probability tree for all possible branch generations
    let manhattan = (end_height + end_length) - base_length - start_height;
    let sequences = repeat_n(vec![false, true], manhattan as usize).multi_cartesian_product();
    let start_height = start_height;

    // Iterate over every possible branch generation
    for seq in sequences {
        let mut temp_manhattan = manhattan;
        let mut remaining_height = end_height;
        let mut remaining_length = end_length - base_length;
        let mut temp_branch_offset = branch_offset;
        let mut temp_logs = [F::from(0); 6];
        let mut chance = F::from(1);

        for value in seq {
            let y_error = (remaining_height - start_height).abs() / temp_manhattan;

            if value {
                // Multiply by y_error to get chance of event occuring
                chance *= y_error;
                // Some combinations aren't always possible...
                if remaining_height > 0 {
                    remaining_height -= 1;
                }
            } else {
                chance *= 1 - y_error;
                if remaining_length > 0 {
                    remaining_length -= 1;
                    temp_branch_offset += 1;
                }
            }

            temp_logs[temp_branch_offset] += 1;
            temp_manhattan -= 1;
        }

        // Add logs in this sequence multiplied by total chance of the sequence
        for index in 0..temp_logs.len() {
            branch_logs[index] += temp_logs[index] * chance;
        }
    }

    branch_logs
}

pub fn generate(
    base_height: i32,
    first_random: i32,
    second_random: i32,
    branch_count: Vec<i32>,
    branch_length: (i32, i32),
    branch_start_offset: (i32, i32),
    branch_end_offset: (i32, i32),
) -> ConfigurationMap {
    let mut map = ConfigurationMap::new();

    let first_rand = 0..=first_random;
    let second_rand = 0..=second_random;
    let branch_count = branch_count;
    let branch_length = (branch_length.0)..=(branch_length.1);
    let f_branch_start_offset = (branch_start_offset.0)..=(branch_start_offset.1);
    let s_branch_start_offset = (branch_start_offset.0)..=(branch_start_offset.1 - 1);
    let branch_end_offset = (branch_end_offset.0)..=(branch_end_offset.1);

    let random_product = iproduct!(
        first_rand,
        second_rand,
        branch_count,
        f_branch_start_offset,
        branch_length.clone(),
        branch_end_offset.clone(),
        s_branch_start_offset,
        branch_length,
        branch_end_offset
    );

    for (
        first,
        second,
        count,
        f_offset,
        f_length,
        f_end_offset,
        s_offset,
        s_length,
        s_end_offset,
    ) in random_product
    {
        let mut logs = vec![F::from(0); 6];

        let height = base_height + first + second;
        let fb_height = height - 1 + f_offset;
        let mut sb_height = height - 1 + s_offset;
        if sb_height >= fb_height {
            sb_height += 1;
        }

        let trunk_height = {
            if count >= 2 {
                if count == 3 {
                    height
                } else {
                    fb_height.max(sb_height) + 1
                }
            } else {
                fb_height + 1
            }
        };
        logs[0] += trunk_height;

        let branch = generate_branch(
            height,
            fb_height,
            fb_height < (trunk_height - 1),
            f_length,
            f_end_offset,
        );

        for index in 0..branch.len() {
            logs[index] += branch[index];
        }

        if count >= 2 {
            let second_branch = generate_branch(
                height,
                sb_height,
                sb_height < (trunk_height - 1),
                s_length,
                s_end_offset,
            );

            for index in 0..second_branch.len() {
                logs[index] += branch[index];
            }
        }

        let key = vec![
            first,
            second,
            count,
            f_offset,
            f_length,
            f_end_offset,
            s_offset,
            s_length,
            s_end_offset,
        ];
        map.insert(key, logs);
    }

    map
}

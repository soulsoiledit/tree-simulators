use itertools::iproduct;

use crate::ConfigurationMap;

// TODO:
pub fn generate(base: i32, first: i32, second: i32) -> ConfigurationMap {
    let mut map = ConfigurationMap::new();
    let first = 0..=first;
    let second = 0..=second;
    let first_branch_height = 1..=4;
    let first_branch_length = 1..=3;
    let second_branch_height = 1..=2;
    let second_branch_length = 1..=3;
    let product = iproduct!(
        first,
        second,
        first_branch_height,
        first_branch_length,
        second_branch_height,
        second_branch_length
    );

    for (
        first_rand,
        second_rand,
        first_branch_height,
        first_branch_length,
        second_branch_height,
        second_branch_length,
    ) in product
    {
        let mut logs = vec![crate::F::from(0); 4];
        let mut branch_len = first_branch_length;
        let mut x_offset = 0;

        let height = base + first_rand + second_rand;
        let base_trunk_height = height - first_branch_height;

        for m in 0..height {
            if m >= base_trunk_height && branch_len > 0 {
                x_offset += 1;
                branch_len -= 1;
            }
            logs[x_offset] += 1;
        }

        x_offset = 0;
        branch_len = second_branch_length;
        let ext_trunk_height = base_trunk_height - second_branch_height;

        for p in ext_trunk_height..height {
            if branch_len <= 0 {
                break;
            }

            if p >= 1 {
                x_offset += 1;
                // Runs only 1/4 of the time
                logs[x_offset] += crate::F::new(3u32, 4u32);
            }

            branch_len -= 1;
        }

        let key = vec![
            first_rand,
            second_rand,
            first_branch_height,
            first_branch_length,
            second_branch_height,
            second_branch_length,
        ];
        map.insert(key, logs);
    }

    map
}

use itertools::iproduct;

use crate::ConfigurationMap;

// TODO:
pub fn generate(
    base_height: i32,
    first_random: i32,
    second_random: i32,
    bend_length: (i32, i32),
) -> ConfigurationMap {
    let mut map = ConfigurationMap::new();
    let first_rand = 0..=first_random;
    let second_rand = 0..=second_random;
    let base_offset = 0..2;
    let bend_len = (bend_length.0)..=(bend_length.1);
    let random_product = iproduct!(first_rand, second_rand, base_offset, bend_len);

    for (first_rand, second_rand, base_offset, bend_len) in random_product {
        let mut logs = vec![crate::F::from(0); 5];
        let mut x_offset = 0;

        let height = base_height + first_rand + second_rand;
        let max_height = height - 1;

        for d in 0..=max_height {
            if d + 1 >= max_height + base_offset {
                x_offset += 1;
            }
            logs[x_offset] += 1;
        }

        for _ in 0..=bend_len {
            logs[x_offset] += 1;
            x_offset += 1;
        }

        let key = vec![first_rand, second_rand, bend_len, base_offset];
        map.insert(key, logs);
    }

    map
}

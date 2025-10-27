use crate::ConfigurationMap;
use itertools::iproduct;

pub fn generate(
    base_height: i32,
    first_random: i32,
    second_random: i32,
    branch_length: (i32, i32),
    branch_probability: f64,
) -> ConfigurationMap {
    let mut map = ConfigurationMap::new();

    let first_random = 0..=first_random;
    let second_random = 0..=second_random;
    let maximum_branch_length = (branch_length.0..=branch_length.1).count() as f64;

    let random_product = iproduct!(first_random, second_random);

    for (first_rand, second_rand) in random_product {
        let mut logs = vec![0.0; maximum_branch_length as usize];
        let height = base_height + first_rand + second_rand;

        // Generate map of average number of logs per branch
        let mut branch_logs = vec![0.0; maximum_branch_length as usize];
        for length in (branch_length.0)..=(branch_length.1) {
            let mut offset = 0;
            let mut remaining_length = length - 1;

            for _ in 1..height {
                if remaining_length <= 0 {
                    break;
                }
                offset += 1;
                branch_logs[offset] += branch_probability;

                remaining_length -= 1;
            }
        }

        logs[0] += height as f64;
        for index in 0..logs.len() {
            logs[index] += branch_logs[index] / maximum_branch_length * (height as f64 - 1.0);
        }

        let key = vec![first_rand, second_rand];
        map.insert(key, logs);
    }

    map
}

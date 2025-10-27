use crate::ConfigurationMap;
use itertools::iproduct;

pub fn generate(base_height: i32, first_random: i32, second_random: i32) -> ConfigurationMap {
    let mut map = ConfigurationMap::new();

    let first_rand = 0..=first_random;
    let second_rand = 0..=second_random;
    let branch_sub = 0..4;
    let branch_length = 0..3;

    let random_product = iproduct!(first_rand, second_rand, branch_sub, branch_length);

    for (first_rand, second_rand, top_offset, length) in random_product {
        let mut logs = vec![0.0; 3];

        let height = base_height + first_rand + second_rand;
        let branch_height = height - top_offset;
        let mut branch_length = 2 - length;
        let mut offset = 0;

        let mut overlap_heights = vec![];
        for pos in 0..height {
            if pos >= branch_height && branch_length > 0 {
                offset += 1;
                branch_length -= 1;
            }

            // Add heights where logs can overlap
            match offset {
                0 => logs[0] += 4.0,
                1 => {
                    logs[0] += 2.0;
                    logs[1] += 2.0;
                    overlap_heights.push(pos);
                }
                _ => {
                    logs[1] += 2.0;
                    logs[2] += 2.0;
                    overlap_heights.push(pos);
                }
            };
        }

        let mut extra_logs = 0;
        for random in 0..3 {
            let s = 2 + random;
            for t in 0..s {
                let temp_height = height - t - 2;

                // Logs can overlap in 1/6 spots at some heights, add 10 instead
                if overlap_heights.contains(&temp_height) {
                    extra_logs += 10;
                } else {
                    extra_logs += 12;
                }
            }
        }
        // Code only runs ~1/9 of the time in real generation, scale down
        logs[1] += extra_logs as f64 / 9.0;

        let key = vec![first_rand, second_rand, top_offset, length];
        map.insert(key, logs);
    }

    map
}

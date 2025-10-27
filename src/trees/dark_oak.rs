use crate::{ConfigurationMap, F};
use itertools::iproduct;

// TODO:
pub fn generate(base: i32, first: i32, second: i32) -> ConfigurationMap {
    let mut map = ConfigurationMap::new();
    let first = 0..=first;
    let second = 0..=second;
    let branch_height = 0..4;
    let branch_length = 0..3;
    let product = iproduct!(first, second, branch_height, branch_length);

    for (first, second, branch_height, branch_length) in product {
        let mut logs = vec![F::from(0); 3];

        let height = base + first + second;
        let branch_height = height - branch_height;
        let mut branch_length = 2 - branch_length;
        let mut offset = 0;

        let mut overlap_heights = vec![];
        for pos in 0..height {
            if pos >= branch_height && branch_length > 0 {
                offset += 1;
                branch_length -= 1;
            }

            // Add heights where logs can overlap
            match offset {
                0 => logs[0] += 4,
                1 => {
                    logs[0] += 2;
                    logs[1] += 2;
                    overlap_heights.push(pos);
                }
                _ => {
                    logs[1] += 2;
                    logs[2] += 2;
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
        logs[1] += F::from(extra_logs) / 9;

        let key = vec![first, second, branch_height, branch_length];
        map.insert(key, logs);
    }

    map
}

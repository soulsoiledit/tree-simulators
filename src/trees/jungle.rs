use std::f64::consts::PI;

use crate::ConfigurationMap;
use crate::F;
use itertools::{iproduct, repeat_n, Itertools};

// TODO:
pub fn generate(base_height: i32, first_random: i32, second_random: i32) -> ConfigurationMap {
    let mut map = ConfigurationMap::new();

    let first_rand = 0..=first_random;
    let second_rand = 0..=second_random;
    let trunk_sub = 0..=3;

    let random_product = iproduct!(first_rand, second_rand, trunk_sub);

    // Old approximate multiplier generation for reference
    // const DIVISIONS: i32 = i16::MAX as i32;
    // const DIVISIONS_FLOAT: f64 = DIVISIONS as f64;
    // let mut branch_multiplier = vec![0.0; 5];
    //
    // for inc in 0..DIVISIONS {
    //     let angle = inc as f64 / DIVISIONS_FLOAT * PI * 2.0;
    //
    //     for length in 0..5 {
    //         let mut x_offset = (1.5 + angle.cos() * length as f64).trunc() as i32;
    //         let mut z_offset = (1.5 + angle.sin() * length as f64).trunc() as i32;
    //
    //         if 0 <= x_offset && x_offset <= 1 && 0 <= z_offset && z_offset <= 1 {
    //             continue;
    //         }
    //         if x_offset > 1 {
    //             x_offset -= 1;
    //         }
    //         if z_offset > 1 {
    //             z_offset -= 1;
    //         }
    //
    //         let total_offset = (x_offset).abs().max(z_offset.abs()) as usize;
    //         branch_multiplier[total_offset] += 1.0;
    //     }
    // }
    // for val in &mut branch_multiplier {
    //     *val /= DIVISIONS_FLOAT;
    // }

    // Exact multipliers were found using lots of bad math
    let asin_1_4 = F::from((1.0 / 4.0f64).asin());
    let asin_3_4 = F::from((3.0 / 4.0f64).asin());
    let asin_1_2 = F::from(PI / 6.0);
    let asin_5_6 = F::from((5.0 / 6.0f64).asin());
    let asin_5_8 = F::from((5.0 / 8.0f64).asin());
    let asin_7_8 = F::from((7.0 / 8.0f64).asin());
    let branch_multiplier: [F; 5] = [
        F::from(0),
        F::new(7u64, 12u64) + (asin_7_8 + asin_1_2 - asin_5_6 + asin_3_4 * 2 - asin_1_4) / PI,
        F::new(5u64, 4u64) + (asin_5_8 - asin_7_8 + asin_5_6 * 2 - asin_1_2 - asin_3_4 * 2) / PI,
        F::new(3u64, 4u64) + (asin_7_8 * 2 - asin_5_8 - asin_5_6 * 2) / PI,
        F::from(1) - (asin_7_8 * 2) / PI,
    ];

    for (first_rand, second_rand, sub) in random_product {
        let mut logs = vec![F::from(0); 5];

        let height = F::from(base_height + first_rand + second_rand);
        logs[0] += height * 4 - 3;

        let branch_height = height - 2 - sub;
        let maximum_iterations: u32 = (height / 4).floor().try_into().unwrap();
        let sequences = repeat_n(vec![0, 1, 2, 3], maximum_iterations.try_into().unwrap())
            .multi_cartesian_product();

        let mut temp_value = 0;
        for sequence in sequences {
            let mut temp_branch_height = F::from(branch_height);
            for step in sequence {
                if temp_branch_height <= (height / 2) {
                    break;
                }
                temp_value += 1;
                temp_branch_height -= 2 + step;
            }
        }

        let temp_scaled = temp_value / 4i32.pow(maximum_iterations);

        for index in 1..logs.len() {
            logs[index] += branch_multiplier[index] * temp_scaled;
        }

        let key = vec![first_rand, second_rand, sub];
        map.insert(key, logs);
    }

    map
}

use crate::ConfigurationMap;
use itertools::{iproduct, repeat_n, Itertools};
use std::f64::consts::PI;

pub fn generate(base_height: i32, first_random: i32, second_random: i32) -> ConfigurationMap {
    let mut map = ConfigurationMap::new();

    let first_rand = 0..=first_random;
    let second_rand = 0..=second_random;
    let trunk_sub = 0..=3;

    let random_product = iproduct!(first_rand, second_rand, trunk_sub);

    // Old approximate multiplier generation
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
    let asin_1_4 = (1.0 / 4.0f64).asin();
    let asin_3_4 = (3.0 / 4.0f64).asin();
    let asin_1_2 = PI / 6.0;
    let asin_5_6 = (5.0 / 6.0f64).asin();
    let asin_5_8 = (5.0 / 8.0f64).asin();
    let asin_7_8 = (7.0 / 8.0f64).asin();
    let branch_multiplier = [
        0.0,
        (7.0 / 12.0) + (asin_7_8 + asin_1_2 - asin_5_6 + 2.0 * asin_3_4 - asin_1_4) / PI,
        1.25 + (asin_5_8 - asin_7_8 + 2.0 * asin_5_6 - asin_1_2 - 2.0 * asin_3_4) / PI,
        0.75 + (2.0 * asin_7_8 - asin_5_8 - 2.0 * asin_5_6) / PI,
        1.0 - (2.0 * asin_7_8) / PI,
    ];

    for (first_rand, second_rand, sub) in random_product {
        let mut logs = vec![0.0; 5];

        let height = (base_height + first_rand + second_rand) as f64;
        logs[0] += 4.0 * height - 3.0;

        let branch_height = height - 2.0 - sub as f64;
        let maximum_iterations = (height / 4.0).floor();
        let sequences = repeat_n(vec![0.0, 1.0, 2.0, 3.0], maximum_iterations as usize)
            .multi_cartesian_product();

        let mut temp_value = 0.0;
        for sequence in sequences {
            let mut temp_branch_height = branch_height;
            for step in sequence {
                if temp_branch_height <= height / 2.0 {
                    break;
                }
                temp_value += 1.0;
                temp_branch_height -= 2.0 + step;
            }
        }
        let temp_scaled = temp_value / 4f64.powf(maximum_iterations);

        for index in 1..logs.len() {
            logs[index] += temp_scaled * branch_multiplier[index];
        }

        let key = vec![first_rand, second_rand, sub];
        map.insert(key, logs);
    }

    map
}

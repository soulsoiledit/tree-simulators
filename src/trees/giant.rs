use itertools::iproduct;

use crate::ConfigurationMap;

pub fn generate(base_height: i32, first_random: i32, second_random: i32) -> ConfigurationMap {
    let mut map = ConfigurationMap::new();

    let first_rand = 0..=first_random;
    let second_rand = 0..=second_random;

    let random_product = iproduct!(first_rand, second_rand);

    for (first_rand, second_rand) in random_product {
        let logs = (4 * (base_height + first_rand + second_rand) - 3) as f64;

        let key = vec![first_rand, second_rand];
        map.insert(key, vec![logs]);
    }

    map
}

use crate::ConfigurationMap;
use itertools::iproduct;

pub fn generate() -> ConfigurationMap {
    let mut map = ConfigurationMap::new();

    let stem_height = 4..=6;
    let should_double = 0..12;
    let random_product = iproduct!(stem_height, should_double);

    for (stem_height, should_double) in random_product {
        let mut blocks = vec![stem_height as f64, 45.0];
        if should_double == 0 {
            blocks[0] *= 2.0;
        }

        let key = vec![stem_height, should_double];
        map.insert(key, blocks);
    }

    map
}

use crate::tree::{Configurations, Tree};
use itertools::iproduct;
use rug::Rational;

pub struct HugeFungus {
    name: String,
}

impl HugeFungus {
    pub fn new(name: &str) -> Self {
        HugeFungus {
            name: name.to_string(),
        }
    }
}

impl Tree for HugeFungus {
    fn name(&self) -> &String {
        &self.name
    }

    fn get_configurations(&self) -> Configurations {
        let mut map = Configurations::new();
        let stem = 4..=13;
        let should_double = 0..12;
        let product = iproduct!(stem, should_double);

        for (mut stem, should_double) in product {
            let key = vec![stem, should_double];
            if should_double == 0 {
                stem *= 2;
            }
            map.insert(key, vec![Rational::from(stem)]);
        }

        map
    }
}

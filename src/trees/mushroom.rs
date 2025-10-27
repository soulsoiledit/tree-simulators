use crate::tree::{Configurations, Tree};
use itertools::iproduct;
use rug::Rational;

const CAP: i32 = 45;

pub struct HugeMushroom {
    name: String,
}

impl HugeMushroom {
    pub fn new(name: &str) -> Self {
        HugeMushroom {
            name: name.to_string(),
        }
    }
}

impl Tree for HugeMushroom {
    fn name(&self) -> &String {
        &self.name
    }

    fn get_configurations(&self) -> Configurations {
        let mut map = Configurations::new();
        let stem = 4..=6;
        let should_double = 0..12;
        let product = iproduct!(stem, should_double);

        for (mut stem, should_double) in product {
            let key = vec![stem, should_double];
            if should_double == 0 {
                stem *= 2;
            }
            map.insert(key, vec![Rational::from(stem), Rational::from(CAP)]);
        }

        map
    }
}

use std::ops::RangeInclusive;

use itertools::iproduct;
use rug::Rational;

use crate::tree::{Configurations, Tree};

pub struct SimpleTree {
    name: String,
    base_height: i32,
    first_random_height: RangeInclusive<i32>,
    second_random_height: RangeInclusive<i32>,
}

impl SimpleTree {
    pub fn new(
        name: &str,
        base_height: i32,
        first_random_height: i32,
        second_random_height: i32,
    ) -> Self {
        SimpleTree {
            name: name.to_string(),
            base_height,
            first_random_height: 0..=first_random_height,
            second_random_height: 0..=second_random_height,
        }
    }
}

impl Tree for SimpleTree {
    fn name(&self) -> &String {
        &self.name
    }

    fn get_configurations(&self) -> Configurations {
        let mut map = Configurations::new();

        let product = iproduct!(
            self.first_random_height.clone(),
            self.second_random_height.clone()
        );

        for (first_height, second_height) in product {
            let key = vec![first_height, second_height];
            let logs = self.base_height + first_height + second_height;

            map.insert(key, vec![Rational::from(logs)]);
        }

        map
    }
}

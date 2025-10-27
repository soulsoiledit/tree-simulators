use rug::Rational;
use std::collections::HashMap;

type RandomState = Vec<i32>;
type BlockRings = Vec<Rational>;
pub type Configurations = HashMap<RandomState, BlockRings>;

pub struct Statistics {
    sums: Vec<Rational>,
    averages: Vec<Rational>,
}

pub trait Tree {
    fn name(&self) -> &String;
    fn get_configurations(&self) -> Configurations;

    fn get_statistics(&self) -> Statistics {
        let configurations = self.get_configurations();

        let num_rings = configurations
            .values()
            .next()
            .expect("Empty configuration!")
            .len();
        let total_configurations = Rational::from(configurations.len());

        let mut sums = vec![Rational::from(0); num_rings];
        let mut averages = vec![Rational::from(0); num_rings];

        for (_, rings) in configurations {
            for (i, blocks) in rings.iter().enumerate() {
                sums[i] += blocks;
            }
        }

        for (i, sum) in sums.iter().enumerate() {
            averages[i] = Rational::from(sum / &total_configurations);
        }

        Statistics { sums, averages }
    }

    fn print_results(&self) {
        let statistics = self.get_statistics();
        println!(
            "{}: {:?} {:?}",
            self.name(),
            statistics.sums,
            statistics.averages
        )
    }
}

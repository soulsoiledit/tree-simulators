use rand::Rng;
use std::collections::HashMap;
use strum::IntoEnumIterator;
use strum_macros::EnumIter;

mod trees;

#[allow(dead_code)]
fn bonemeal(attempts: i64) {
    let tenth_of_attempts: i64 = attempts / 10;
    const BONEMEAL_ATTEMPTS: f32 = 3.0;
    const CLOCK_SPEED: i32 = 4;
    const TREES_PLANTED: f32 = 72000.0 / CLOCK_SPEED as f32;

    let mut successes = 0;
    let mut growth_stage = 0;
    let mut rand = rand::rng();

    for i in 0..attempts {
        let mut n = 0.0;

        while n < BONEMEAL_ATTEMPTS {
            let random: f32 = rand.random();

            if random <= 0.45 {
                growth_stage += 1;
            }

            n += 1.0;
            if growth_stage >= 2 {
                successes += 1;
                growth_stage = 0;
                break;
            }
        }

        if (i % tenth_of_attempts) == 0 && i > 0 {
            println!("{successes} / {i} = {}", successes as f32 / i as f32);
        }
    }

    let success_rate: f64 = successes as f64 / attempts as f64;
    println!("{successes} / {attempts} = {}", success_rate);
    println!("{}", success_rate * TREES_PLANTED as f64);
}

#[derive(Debug, EnumIter)]
enum Tree {
    Birch,
    Oak,
    Jungle,
    Spruce,

    Acacia,
    Azalea,
    Cherry,

    Fungus,
    Mushroom,

    MegaSpruce,
    DarkOak,
    MegaJungle,

    Mangrove,
    TallMangrove,

    Pine,
    MegaPine,
    TallBirch,
    SwampOak,
    JungleBush,
}

type ConfigurationMap = HashMap<Vec<i32>, Vec<f64>>;

fn get_average(configuration: ConfigurationMap) -> String {
    let value_length = configuration.values().next().unwrap().len();
    let mut sums = vec![0.0; value_length];
    for entry in configuration.values() {
        for index in 0..value_length {
            sums[index] += entry[index];
        }
    }

    let mut averages = vec![];
    for sum in &sums {
        averages.push(sum / configuration.len() as f64);
    }

    format!("{} {:?} {:?}", configuration.len(), sums, averages)
}

fn main() {
    for tree_type in Tree::iter() {
        let tree_configurations = match tree_type {
            Tree::Birch => trees::simple::generate(5, 2, 0),
            Tree::Oak => trees::simple::generate(4, 2, 0),
            Tree::Jungle => trees::simple::generate(4, 8, 0),
            Tree::Spruce => trees::simple::generate(5, 2, 1),

            Tree::Acacia => trees::acacia::generate(5, 2, 2),
            Tree::Azalea => trees::azalea::generate(4, 2, 0, (1, 2)),
            Tree::Cherry => {
                trees::cherry::generate(7, 1, 0, vec![1, 2, 3], (2, 4), (-4, -3), (-1, 0))
            }

            Tree::Fungus => trees::fungus::generate(),
            Tree::Mushroom => trees::mushroom::generate(),

            Tree::MegaSpruce => trees::giant::generate(13, 2, 14),
            Tree::DarkOak => trees::dark_oak::generate(6, 2, 1),
            Tree::MegaJungle => trees::jungle::generate(10, 2, 19),

            Tree::Mangrove => trees::mangrove::generate(2, 1, 4, (1, 4), 0.5),
            Tree::TallMangrove => trees::mangrove::generate(4, 1, 9, (1, 6), 0.5),

            Tree::Pine => trees::simple::generate(6, 4, 0),
            Tree::MegaPine => trees::giant::generate(13, 2, 14),
            Tree::TallBirch => trees::simple::generate(5, 2, 6),
            Tree::SwampOak => trees::simple::generate(5, 3, 0),
            Tree::JungleBush => trees::simple::generate(1, 0, 0),
        };
        println!("{:?}: {}", tree_type, get_average(tree_configurations));
    }
}

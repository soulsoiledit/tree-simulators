mod tree;
mod trees;

use rand::Rng;

use crate::tree::Tree;
use crate::trees::fungus::HugeFungus;
use crate::trees::giant::GiantTree;
use crate::trees::mushroom::HugeMushroom;
use crate::trees::simple::SimpleTree;

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

fn main() {
    let trees: Vec<Box<dyn Tree>> = vec![
        Box::new(SimpleTree::new("Birch", 5, 2, 0)),
        Box::new(SimpleTree::new("Oak", 4, 2, 0)),
        Box::new(SimpleTree::new("Jungle", 4, 8, 0)),
        Box::new(SimpleTree::new("Spruce", 5, 2, 1)),
        // Tree::Acacia => trees::acacia::generate(5, 2, 2),
        // Tree::Azalea => trees::azalea::generate(4, 2, 0, (1, 2)),
        // Tree::Cherry => {
        //     trees::cherry::generate(7, 1, 0, vec![1, 2, 3], (2, 4), (-4, -3), (-1, 0))
        // }
        //
        Box::new(HugeFungus::new("Huge Fungus")),
        Box::new(HugeMushroom::new("Huge Mushroom")),
        //
        Box::new(GiantTree::new("2x2 Spruce", 13, 2, 14)),
        // Tree::DarkOak => trees::dark_oak::generate(6, 2, 1),
        // Tree::MegaJungle => trees::jungle::generate(10, 2, 19),
        //
        // Tree::Mangrove => trees::mangrove::generate(2, 1, 4, (1, 4), 0.5),
        // Tree::TallMangrove => trees::mangrove::generate(4, 1, 9, (1, 6), 0.5),
        //
        Box::new(SimpleTree::new("Pine", 6, 4, 0)),
        Box::new(GiantTree::new("2x2 Pine", 13, 2, 14)),
        Box::new(SimpleTree::new("Tall Birch", 5, 2, 6)),
        Box::new(SimpleTree::new("Swamp Oak", 5, 3, 0)),
        Box::new(SimpleTree::new("Jungle Bush", 1, 0, 0)),
    ];

    for tree in trees {
        tree.print_results();
    }
}

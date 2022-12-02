
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::BinaryHeap;


fn main() {
    // read input
    let file = File::open("input").unwrap();
    let mut total: u32 = 0;
    let mut most: BinaryHeap<u32> = BinaryHeap::new();
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let trimmed = line_string.trim();
            if trimmed.len() == 0 {
                most.push(total);
                total = 0;
            } else {
                let value: u32 = trimmed.parse().expect("number");
                total += value;
            }
        }
    }

    // part 1
    println!("{}", most.peek().unwrap());

    // part 2
    let mut top_3: u32 = 0;
    for _ in 0 .. 3 {
        top_3 += most.pop().unwrap();
    }
    println!("{}", top_3);
}

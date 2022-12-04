
use std::fs::File;
use std::io::{self, BufRead};


fn split_pair(text: &str) -> (u32, u32) {
    let mut parts = text.split('-');
    let part1 = parts.next().unwrap();
    let part2 = parts.next().unwrap();
    let num1 = part1.parse().expect("num1");
    let num2 = part2.parse().expect("num2");
    return (num1, num2);
}

fn part1() {
    let file = File::open("input").unwrap();
    let mut part1_total: u32 = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let trimmed = line_string.trim();
            let mut pairs = trimmed.split(',');
            let pair1 = pairs.next().unwrap();
            let pair2 = pairs.next().unwrap();
            let (a, b) = split_pair(pair1);
            let (c, d) = split_pair(pair2);
            if (a <= c) && (b >= d) {
                // pair1 contains pair2
                part1_total += 1;
            } else if (c <= a) && (d >= b) {
                // pair2 contains pair1
                part1_total += 1;
            }
        }
    }

    println!("{}", part1_total);
}

fn main() {
    part1();
}

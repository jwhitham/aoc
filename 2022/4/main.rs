
use std::fs::File;
use std::io::{self, BufRead};


fn split_pair(text: &str) -> (u32, u32) {
    let mut parts = text.split('-');
    let num1 = parts.next().unwrap().parse().expect("num1");
    let num2 = parts.next().unwrap().parse().expect("num2");
    return (num1, num2);
}

fn main() {
    let file = File::open("input").unwrap();
    let mut part1_total: u32 = 0;
    let mut part2_total: u32 = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let mut pairs = line_string.trim().split(',');
            let (a, b) = split_pair(pairs.next().unwrap());
            let (c, d) = split_pair(pairs.next().unwrap());
            if (a <= c) && (b >= d) {
                // pair1 contains pair2
                part1_total += 1;
            } else if (c <= a) && (d >= b) {
                // pair2 contains pair1
                part1_total += 1;
            }
            if (d < a) || (b < c) {
                // no overlap
            } else {
                // at least one overlap
                part2_total += 1;
            }
        }
    }

    println!("{}", part1_total);
    println!("{}", part2_total);
}

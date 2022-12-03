
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;


fn priority(ch: char) -> u32 {
    let value: u32 = ch.into();
    if ch >= 'a' && ch <= 'z' {
        let sub: u32 = 'a'.into();
        return (value - sub) + 1;
    } else if ch >= 'A' && ch <= 'Z' {
        let sub: u32 = 'A'.into();
        return (value - sub) + 27;
    } else {
        panic!();
    }
}

fn main() {
    let file = File::open("input").unwrap();
    let mut part1_total: u32 = 0;
    let mut repeat: HashSet<char> = HashSet::new();
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let trimmed = line_string.trim();
            assert!((trimmed.len() % 2) == 0);

            let half_index = trimmed.len() / 2;
            repeat.clear();
            for ch in trimmed[0 .. half_index].chars() {
                repeat.insert(ch);
            }
            for ch in trimmed[half_index .. trimmed.len()].chars() {
                if repeat.contains(&ch) {
                    repeat.remove(&ch);
                    part1_total += priority(ch);
                }
            }
        }
    }

    println!("{}", part1_total);
}

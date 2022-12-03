
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;
use std::collections::HashMap;


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

fn part1() {
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

fn part2() {
    let file = File::open("input").unwrap();
    let mut part2_total: u32 = 0;
    let mut present: HashMap<char, u8> = HashMap::new();
    let mut group_bit: u8 = 1;
    const ELVES_PER_GROUP: u8 = 3;

    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let trimmed = line_string.trim();
            assert!((trimmed.len() % 2) == 0);

            for ch in trimmed.chars() {
                present.insert(ch, present.get(&ch).unwrap_or(&0)
                                       | group_bit);
            }
            group_bit = group_bit << 1;
            if group_bit >= (1 << ELVES_PER_GROUP) {
                for (ch, bits) in present.drain() {
                    if bits == (1 << ELVES_PER_GROUP) - 1 {
                        // carried by all elves!
                        part2_total += priority(ch);
                    }
                }

                assert!(present.is_empty());
                group_bit = 1;
            }
        }
    }
    assert!(group_bit == 1);

    println!("{}", part2_total);
}

fn main() {
    part1();
    part2();
}

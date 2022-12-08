
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;


type Word = i8;
type Height = u8;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Location {
    x: Word,
    y: Word,
}

fn part1(filename: &str) -> u32 {
    let file = File::open(filename).unwrap();
    let mut y: Word = 0;
    let mut x: Word = 0;
    let mut forest: HashMap<Location, Height> = HashMap::new();
    for line in io::BufReader::new(file).lines() {
        x = 0;
        if let Ok(line_string) = line {
            for ch in line_string.chars() {
                forest.insert(Location { x: x, y: y }, ch as Height);
                x += 1;
            }
        }
        y += 1;
    }
    let width = x;
    let height = y;

    fn scan_vector(forest: &HashMap<Location, Height>, start_loc: &Location,
                   dx: Word, dy: Word) -> bool {
        let mut copy: Location = *start_loc;
        let start_height = forest.get(&copy).unwrap();

        loop {
            copy.x += dx;
            copy.y += dy;
            if let Some (height) = forest.get(&copy) {
                if *height >= *start_height {
                    return false;
                }
            } else {
                return true;
            }
        }
    }

    let mut visible_count: u32 = 0;
    for ty in 0 .. height {
        for tx in 0 .. width {
            let l = Location { x: tx, y: ty };
            if scan_vector(&forest, &l, -1, 0)
            || scan_vector(&forest, &l, 1, 0)
            || scan_vector(&forest, &l, 0, -1)
            || scan_vector(&forest, &l, 0, 1) {
                visible_count += 1;
            }
        }
    }

    return visible_count;
}

#[test]
fn test_part1() {
    assert_eq!(part1("test21"), 21);
}

fn main() {
    println!("{}", part1("input"));
}




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


type Forest = HashMap<Location, Height>;

fn read_input(filename: &str) -> (Forest, Word, Word) {
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
    return (forest, x, y);
}

fn part1(filename: &str) -> u32 {
    let (forest, width, height) = read_input(filename);

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

fn part2(filename: &str) -> u32 {
    let (forest, width, height) = read_input(filename);

    fn scan_vector(forest: &HashMap<Location, Height>,
                   start_loc: &Location,
                   dx: Word, dy: Word) -> u32 {

        let mut copy: Location = *start_loc;
        let start_height = forest.get(&copy).unwrap();
        let mut distance: u32 = 0;

        loop {
            copy.x += dx;
            copy.y += dy;
            if let Some (height) = forest.get(&copy) {
                distance += 1;
                if *height >= *start_height {
                    // can't see beyond this
                    return distance;
                }
            } else {
                // reached the edge
                return distance;
            }
        }
    }

    let mut best_score: u32 = 0;
    for ty in 0 .. height {
        for tx in 0 .. width {
            let l = Location { x: tx, y: ty };
            let c = scan_vector(&forest, &l, -1, 0)
                * scan_vector(&forest, &l, 1, 0)
                * scan_vector(&forest, &l, 0, -1)
                * scan_vector(&forest, &l, 0, 1);
            best_score = u32::max(best_score, c);
        }
    }

    return best_score;
}

#[test]
fn test_part2() {
    assert_eq!(part2("test21"), 8);
}


fn main() {
    println!("{}", part1("input"));
    println!("{}", part2("input"));
}



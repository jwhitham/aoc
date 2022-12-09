
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;
use std::iter::FromIterator;


type Word = i16;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Location {
    x: Word,
    y: Word,
}

type Path = Vec<Location>;
type Visited = HashSet<Location>;

fn read_input(filename: &str) -> Path {
    let file = File::open(filename).unwrap();
    let mut locations: Path = Vec::new();
    let mut loc = Location { x: 0, y: 0, };
    locations.push(loc);
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let words = Vec::from_iter(line_string.split_ascii_whitespace());
            assert!(words.len() == 2);
            let distance: Word = words.get(1).unwrap().parse().expect("number");
            let direction: &str = *words.get(0).unwrap();
            for _ in 0 .. distance {
                match direction {
                    "U" => { loc.y -= 1; },
                    "D" => { loc.y += 1; },
                    "L" => { loc.x -= 1; },
                    "R" => { loc.x += 1; },
                    _ => panic!(),
                }
                locations.push(loc);
            }
        }
    }
    return locations;
}

fn sign(d: Word) -> Word {
    if d > 0 {
        return 1;
    } else if d < 0 {
        return -1;
    } else {
        return 0;
    }
}

fn step(d1: Word, d2: Word) -> Word {
    match Word::abs(d1) {
        2 => {
            // Always step in the right direction if it's 2 away
            return sign(d1);
        },
        1 => match Word::abs(d2) {
            2 => {
                // Also step in the right direction if it's 1 away
                // but 2 away in the other dimension
                return sign(d1);
            },
            1 | 0 => {
                // Close enough, no move in this dimension
                return 0;
            },
            _ => {
                panic!();
            },
        },
        0 => {
            return 0;
        },
        _ => {
            panic!();
        },
    }
}

fn part1(filename: &str) -> usize {
    let locations = read_input(filename);

    let mut tail = *locations.get(0).unwrap();
    let mut visited = Visited::new();

    for head in locations {
        let dx = head.x - tail.x;
        let dy = head.y - tail.y;
        tail.x += step(dx, dy);
        tail.y += step(dy, dx);
        visited.insert(tail);
        // At most 1 space away in each direction
        assert!(Word::abs(tail.x - head.x) <= 1);
        assert!(Word::abs(tail.y - head.y) <= 1);
    }
    return visited.len();
}

#[test]
fn test_part1() {
    assert_eq!(part1("test13"), 13);
}


fn main() {
    println!("{}", part1("input"));
}



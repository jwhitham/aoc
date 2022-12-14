
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;
use std::iter::FromIterator;


type Word = i32;

#[derive(Copy, Clone, Hash, Eq, PartialEq)]
struct Location {
    x: Word,
    y: Word,
}

type Map = HashSet<Location>;

struct Problem {
    map: Map,
    max_y: Word,
}

fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p = Problem {
        map: HashSet::new(),
        max_y: 0,
    };
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let cleaned = line_string.replace("->", " ")
                                     .replace(",", " ");
            let fields = Vec::from_iter(cleaned.split_ascii_whitespace());
            let pairs = fields.len() / 2;
            let mut x1: Word = fields.get(0).unwrap().parse().expect("x1");
            let mut y1: Word = fields.get(1).unwrap().parse().expect("y1");
            assert!(pairs > 1);

            for i in 1 .. pairs {
                let j = i * 2;
                let x2: Word = fields.get(j + 0).unwrap().parse().expect("x2");
                let y2: Word = fields.get(j + 1).unwrap().parse().expect("y2");
                if x1 == x2 {
                    // vertical
                    for y in Word::min(y1, y2) .. Word::max(y1, y2) + 1 {
                        p.map.insert(Location { x: x1, y: y });
                    }
                } else if y1 == y2 {
                    // horizontal
                    for x in Word::min(x1, x2) .. Word::max(x1, x2) + 1 {
                        p.map.insert(Location { x: x, y: y1 });
                    }
                } else {
                    panic!();
                }
                p.max_y = Word::max(Word::max(y1, y2), p.max_y);
                x1 = x2;
                y1 = y2;
            }
        }
    }
    return p;
}

fn part1(p: &mut Problem) -> usize {
    let mut sand_count: usize = 0;
    loop {
        sand_count += 1;
        let mut sand_x: Word = 500;
        let mut sand_y: Word = 0;
        assert!(!p.map.contains(&Location { x: sand_x, y: sand_y }));
        loop {
            if !p.map.contains(&Location { x: sand_x, y: sand_y + 1 }) {
                sand_y += 1;
            } else if !p.map.contains(&Location { x: sand_x - 1, y: sand_y + 1 }) {
                sand_x -= 1;
                sand_y += 1;
            } else if !p.map.contains(&Location { x: sand_x + 1, y: sand_y + 1 }) {
                sand_x += 1;
                sand_y += 1;
            } else {
                // sand is stuck
                p.map.insert(Location { x: sand_x, y: sand_y });
                break;
            }
            if sand_y > p.max_y {
                // now fallen to the void
                return sand_count - 1;
            }
        }
    }
}

#[test]
fn test_part1() {
    assert_eq!(part1(&mut load("test24")), 24);
}

fn main() {
    println!("{}", part1(&mut load("input")));
}



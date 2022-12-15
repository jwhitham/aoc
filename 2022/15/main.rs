
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::cmp::Ordering;



type Word = i32;

#[derive(Copy, Clone)]
struct Location {
    x: Word,
    y: Word,
}

#[derive(Copy, Clone)]
struct Input {
    beacon: Location,
    sensor: Location,
}

type Problem = Vec<Input>;

fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p = Vec::new();
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let cleaned = line_string.replace("=", " ")
                                     .replace(",", " ")
                                     .replace(":", " ");
            let fields = Vec::from_iter(cleaned.split_ascii_whitespace());
            assert!(*fields.get(2).unwrap() == "x");
            assert!(*fields.get(4).unwrap() == "y");
            assert!(*fields.get(10).unwrap() == "x");
            assert!(*fields.get(12).unwrap() == "y");
            p.push(Input {
                sensor: Location {
                    x: fields.get(3).unwrap().parse().expect("sx"),
                    y: fields.get(5).unwrap().parse().expect("sy"),
                },
                beacon: Location {
                    x: fields.get(11).unwrap().parse().expect("bx"),
                    y: fields.get(13).unwrap().parse().expect("by"),
                },
            });
        }
    }
    return p;
}

#[derive(Copy, Clone, Hash)]
struct Exclude {
    x: Word,
    delta: i8,
}

impl Eq for Exclude {}

impl PartialEq for Exclude {
    fn eq(&self, other: &Self) -> bool {
        return self.cmp(other) == Ordering::Equal;
    }
}

impl PartialOrd for Exclude {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        return Some(self.cmp(other));
    }
}

impl Ord for Exclude {
    fn cmp(&self, other: &Self) -> Ordering {
        let c1 = self.x.cmp(&other.x);
        if c1 != Ordering::Equal {
            return c1;
        }
        return other.delta.cmp(&self.delta);
    }
}

fn get_excludes(problem: &Problem, line_y: Word) -> Vec<Exclude> {
    let mut excludes: Vec<Exclude> = Vec::new();
    for input in problem.iter() {
        let beacon_distance =
            Word::abs(input.beacon.x - input.sensor.x) +
            Word::abs(input.beacon.y - input.sensor.y);
        let line_y_distance =
            Word::abs(line_y - input.sensor.y);
        let overlap = beacon_distance - line_y_distance;

        if overlap <= 0 {
            // irrelevant input
            continue;
        }
        let x1 = input.sensor.x - overlap;
        let x2 = input.sensor.x + overlap;
        excludes.push(Exclude { x: x1, delta: 1 });
        excludes.push(Exclude { x: x2, delta: -1 });
    }

    excludes.sort();

    let mut c_excludes: Vec<Exclude> = Vec::new();
    let mut combined = Exclude { x: Word::MIN, delta: 0 };

    // Combine points
    for exclude in excludes.iter() {
        if combined.x == exclude.x {
            combined.delta += exclude.delta;
        } else {
            if combined.x != Word::MIN {
                c_excludes.push(combined);
            }
            combined = *exclude;
        }
    }
    assert!(combined.x != Word::MIN);
    c_excludes.push(combined);
    return c_excludes;
}

fn part1(problem: &Problem, line_y: Word) -> Word {

    let c_excludes = get_excludes(problem, line_y);
    let mut value: i8 = 0;
    let mut start = Exclude { x: Word::MIN, delta: 0 };
    let mut covered_size: Word = 0;

    // Any range with value == 0 could contain a beacon
    for exclude in c_excludes.iter() {
        assert!(value >= 0);
        let was_0: bool = value == 0;
        value += exclude.delta;
        let is_0: bool = value == 0;
        assert!(value >= 0);

        if !is_0 && was_0 {
            // covered part begins
            start = *exclude;
        } else if !was_0 && is_0 && (start.x != Word::MIN) {
            // covered part ends 
            let end = exclude;
            covered_size += end.x - start.x;
            start.x = Word::MIN;
        }
    }
    return covered_size;
}

#[test]
fn test_part1() {
    assert_eq!(part1(&load("test"), 10), 26);
}

fn part2(problem: &Problem, x_y_limit: Word) -> u64 {
    let mut gap: u64 = u64::MAX;

    // Search each line for a gap of size 1
    // Surely there will be a much better way of doing this... however, this
    // produces an answer faster than I can think of a better solution.
    for y in 0 .. x_y_limit {
        let c_excludes = get_excludes(problem, y);

        let mut value: i8 = 0;
        let mut start = Exclude { x: Word::MIN, delta: 0 };

        for exclude in c_excludes.iter() {
            assert!(value >= 0);
            let was_0: bool = value == 0;
            value += exclude.delta;
            let is_0: bool = value == 0;
            assert!(value >= 0);

            if !was_0 && is_0 {
                // gap begins
                start = *exclude;
            } else if !is_0 && was_0 && (start.x != Word::MIN) {
                // gap ends
                let end = exclude;
                let gap_size = end.x - start.x - 1;
                if (end.x > 0) && (start.x <= x_y_limit) {
                    // gap is within the area of interest
                    if gap_size > 0 {
                        // Only looking for one gap of size 1
                        assert!(gap == u64::MAX);   // more than one gap found
                        assert_eq!(gap_size, 1);    // gap is too large
                        gap = (((end.x as u64) - 1) * 4000000) + (y as u64);
                    }
                }
                start.x = Word::MIN;
            }
        }
    }
    assert!(gap != u64::MAX); // no gaps found
    return gap;
}

#[test]
fn test_part2() {
    assert_eq!(part2(&load("test"), 20), 56000011);
}

fn main() {
    println!("{}", part1(&load("input"), 2000000));
    println!("{}", part2(&load("input"), 4000000));
}



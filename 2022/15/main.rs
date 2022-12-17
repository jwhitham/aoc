
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::cmp::Ordering;
use std::collections::HashSet;



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

type Coverage = i8;
type SensorIndex = u8;

#[derive(Copy, Clone, Hash)]
struct Exclude {
    x: Word,
    delta: Coverage,
    index: SensorIndex,
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

fn get_excludes_part1(problem: &Problem, line_y: Word) -> Vec<Exclude> {
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
        excludes.push(Exclude { x: x1, delta: 1, index: 0 });
        excludes.push(Exclude { x: x2, delta: -1, index: 0 });
    }

    excludes.sort();

    let mut c_excludes: Vec<Exclude> = Vec::new();
    let mut combined = Exclude { x: Word::MIN, delta: 0, index: 0 };

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

    let c_excludes = get_excludes_part1(problem, line_y);
    let mut value: i8 = 0;
    let mut start = Exclude { x: Word::MIN, delta: 0, index: 0 };
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

type SensorSet = HashSet<SensorIndex>;

fn make_coverage(diagonal: &Vec<Exclude>) -> Vec<SensorSet> {
    let mut c = SensorSet::new();
    let mut result: Vec<SensorSet> = Vec::new();
    for d in diagonal.iter() {
        let ok: bool = match d.delta {
            1 => c.insert(d.index),
            -1 => c.remove(&d.index),
            _ => false,
        };
        assert!(ok);
        result.push(c.clone());
    }
    let last = result.pop().unwrap();
    assert!(last.is_empty());
    return result;
}

#[derive(Copy, Clone, Eq, PartialEq, Hash)]
struct Uncovered {
    p1: Word, p2: Word, n1: Word, n2: Word,
}

#[derive(Copy, Clone)]
struct Rectangle {
    x1: Word, y2: Word,
    x3: Word, y4: Word,
}

fn calc_bounds(u: &Uncovered) -> Rectangle {
    let x1 = (u.p1 + u.n1) / 2;   // left corner is at (x1, y1)
    let x2 = (u.p2 + u.n1) / 2;   // bottom corner is at (x2, y2)
    let x3 = (u.p2 + u.n2) / 2;   // right corner is at (x3, y3)
    let x4 = (u.p1 + u.n2) / 2;   // top corner is at (x4, y4)
    return Rectangle {
        x1: x1, y2: x2 - u.p2,
        x3: x3, y4: x4 - u.p1,
    };
}

fn check_line(problem: &Problem, y: Word, x_y_limit: Word, found: &mut u64) {
    let c_excludes = get_excludes_part1(problem, y);

    let mut value: i8 = 0;
    let mut start = Exclude { x: Word::MIN, delta: 0, index: 0 };

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
                    assert!(*found == u64::MAX); // more than one gap found
                    assert_eq!(gap_size, 1);        // gap is too large
                    *found = (((end.x as u64) - 1) * 4000000) + (y as u64);
                }
            }
        }
    }
}

fn part2(problem: &Problem, x_y_limit: Word) -> u64 {
   
    // Multiply all coordinates by 2 to avoid rounding errors when
    // we convert between diagonal lines and cells
    let m = 2;

    // Divide up the search space with diagonal lines
    let mut positive: Vec<Exclude> = Vec::new();    // diagonal with dy/dx = 1
    let mut negative: Vec<Exclude> = Vec::new();    // diagonal with dy/dx = -1

    for i in 0 .. problem.len() as SensorIndex {
        let input: &Input = problem.get(i as usize).unwrap();
        let beacon_distance =
            Word::abs(input.beacon.x - input.sensor.x) +
            Word::abs(input.beacon.y - input.sensor.y);

        // First positive diagonal runs through
        // ((input.sensor.x - beacon_distance), input.sensor.y)
        let x1 = input.sensor.x - beacon_distance;
        let y1 = input.sensor.y;

        // and given that dy/dx = 1, it therefore crosses y=0 at:
        let xp = (x1 - y1) * m;
        positive.push(Exclude { x: xp, delta: 1, index: i });

        // second positive diagonal is 2 * beacon_distance further on
        positive.push(Exclude { x: xp + (beacon_distance * 2 * m), delta: -1, index: i });

        // First negative diagonal also runs through (x1, y1)
        // and given that dy/dx = -1, it therefore crosses y=0 at:
        let xn = (x1 + y1) * m;
        negative.push(Exclude { x: xn, delta: 1, index: i });

        // second negative diagonal is 2 * beacon_distance further on
        negative.push(Exclude { x: xn + (beacon_distance * 2 * m), delta: -1, index: i });
    }

    positive.sort();
    negative.sort();
    assert_eq!(negative.len(), positive.len());
    let grid_size = negative.len();

    // This has created a grid of diagonal lines, consisting of rectangles of
    // various sizes. Every point within a rectangle is covered by the same
    // number of sensors. Work out which sensors apply to each rectangle. We treat the two
    // diagonal dimensions separately here. 
    let positive_coverage = make_coverage(&positive);
    let negative_coverage = make_coverage(&negative);
    assert_eq!(grid_size, positive_coverage.len() + 1);
    assert_eq!(grid_size, negative_coverage.len() + 1);

    // Find rectangles with no coverage and non-zero area
    let mut found: u64 = u64::MAX;
    for pi in 0 .. grid_size - 1 {
        let a = positive.get(pi + 0).unwrap().x; // First positive diagonal runs through (a, 0)
        let b = positive.get(pi + 1).unwrap().x; // Second positive (b, 0)
        assert_eq!(a % m, 0);
        assert_eq!(b % m, 0);
        if a == b {
            // area is 0
            continue;
        }
        let pc = positive_coverage.get(pi).unwrap();
        for ni in 0 .. grid_size - 1 {
            let c = negative.get(ni + 0).unwrap().x; // First negative (c, 0)
            let d = negative.get(ni + 1).unwrap().x; // Second negative (d, 0)
            assert_eq!(c % m, 0);
            assert_eq!(d % m, 0);
            if c == d {
                // area is 0
                continue;
            }
            let nc = negative_coverage.get(ni).unwrap();
            let mut covered_by = pc.intersection(&nc);
            if covered_by.next().is_some() {
                // rectangle is covered
                continue;
            }
            // Check that it's in the valid region
            let new_uncovered = Uncovered { p1: a, n1: c, p2: b, n2: d };
            let bounds = calc_bounds(&new_uncovered);
            if (bounds.x1 >= (m * x_y_limit)) || (bounds.x3 <= 0)
            || (bounds.y2 >= (m * x_y_limit)) || (bounds.y4 <= 0) {
                // rectangle is entirely outside the space of interest
                continue;
            }

            // Having found an uncovered rectangle, we may now be able to say that
            // the desired point is right in the middle of it... however, the rectangle
            // can be split in half (or even into quarters) by other lines,
            // so the simplest way to find the desired point is to scan all of the lines.
            // Seems a little unsatisfying but merging the rectangles together is pretty difficult
            // and not worth it for the negligible saved time. We already cut down the
            // problem size massively.
            for y in (bounds.y2 / m) + 1 .. bounds.y4 / m {
                check_line(problem, y, x_y_limit, &mut found);
            }
        }
    }
    assert!(found != u64::MAX);   // found none
    return found;
}

#[test]
fn test_part2() {
    assert_eq!(part2(&load("test"), 20), 56000011);
}

fn main() {
    println!("{}", part1(&load("input"), 2000000));
    println!("{}", part2(&load("input"), 4000000));
}



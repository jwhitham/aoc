
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashSet;
use std::collections::BinaryHeap;
use std::cmp::Ordering;

type Word = i32;
type Time = u32;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Location {
    x: Word,
    y: Word,
}

#[derive(Eq, PartialEq, Copy, Clone)]
struct Vector {
    dx: i8,
    dy: i8,
}

#[derive(Eq, PartialEq, Copy, Clone)]
struct Blizzard {
    loc: Location,
    dir: Vector,
}

struct Problem {
    blizzards: Vec<Blizzard>,
    width: Word,
    height: Word,
}

fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p = Problem {
        blizzards: Vec::new(),
        width: 0,
        height: 0,
    };
    let mut y: Word = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let bytes = Vec::from_iter(line_string.bytes());
            let mut x: Word = 0;
            for b in bytes.iter() {
                match *b {
                    b'<' | b'>' | b'^' | b'v' => {
                        p.blizzards.push(Blizzard {
                            loc: Location { x: x, y: y, },
                            dir: match *b {
                                b'<' => Vector { dx: -1, dy: 0 },
                                b'>' => Vector { dx: 1, dy: 0 },
                                b'^' => Vector { dx: 0, dy: -1 },
                                _    => Vector { dx: 0, dy: 1 },
                            },
                        });
                    },
                    b'#' => {
                        p.width = Word::max(p.width, x + 1);
                        p.height = Word::max(p.height, y + 1);
                    },
                    _ => {},
                }
                x += 1;
            }
            y += 1;
        }
    }
    return p;
}

type BlizzardMap = HashSet<Location>;

struct BlizzardMaps {
    north: BlizzardMap,
    east: BlizzardMap,
    south: BlizzardMap,
    west: BlizzardMap,
}

#[derive(Hash, Copy, Clone, Eq, PartialEq)]
struct Location3D {
    x: Word,
    y: Word,
    t: Time,
}

#[derive(Hash, Copy, Clone)]
struct HeapItem {
    loc: Location3D,
    goal: Location,
}

impl Eq for HeapItem {}

impl PartialEq for HeapItem {
    fn eq(&self, other: &Self) -> bool {
        return self.cmp(other) == Ordering::Equal;
    }
}

impl PartialOrd for HeapItem {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        return Some(self.cmp(other));
    }
}

impl Ord for HeapItem {
    fn cmp(&self, other: &Self) -> Ordering {
        // Need a min-heap so the order is reversed
        if self.loc.t > other.loc.t {
            return Ordering::Less;      // Prefer other to self
        } else if self.loc.t < other.loc.t {
            return Ordering::Greater;   // Prefer self to other
        } else {
            // A-star heuristic: Manhattan distance from goal
            let self_d = Word::abs(self.loc.x - self.goal.x) +
                         Word::abs(self.loc.y - self.goal.y);
            let other_d = Word::abs(other.loc.x - other.goal.x) +
                         Word::abs(other.loc.y - other.goal.y);

            if self_d > other_d {
                return Ordering::Less;      // Prefer other to self
            } else if self_d < other_d {
                return Ordering::Greater;   // Prefer self to other
            } else {
                return Ordering::Equal;
            }
        }
    }
}

fn make_blizzard_map(p: &Problem, dir: &Vector) -> BlizzardMap {
    let mut bm = BlizzardMap::new();

    for b in p.blizzards.iter() {
        if b.dir == *dir {
            bm.insert(b.loc);
        }
    }
    return bm;
}

fn make_blizzard_maps(p: &Problem) -> BlizzardMaps {
    return BlizzardMaps {
        north: make_blizzard_map(p, &Vector { dx: 0, dy: -1 }),
        south: make_blizzard_map(p, &Vector { dx: 0, dy: 1 }),
        east:  make_blizzard_map(p, &Vector { dx: 1, dy: 0 }),
        west:  make_blizzard_map(p, &Vector { dx: -1, dy: 0 }),
    };
}

fn is_in_blizzard(p: &Problem, bm: &BlizzardMap, dir: &Vector, loc: &Location3D) -> bool {
    // The blizzard moves one "dir" per time unit
    let bl = Location {
        x: Word::rem_euclid(-((dir.dx as Word) * (loc.t as Word)) + loc.x - 1, p.width - 2) + 1,
        y: Word::rem_euclid(-((dir.dy as Word) * (loc.t as Word)) + loc.y - 1, p.height - 2) + 1,
    };
    return bm.contains(&bl);
}

fn can_move_to(p: &Problem, bms: &BlizzardMaps, loc: &Location3D) -> bool {
    // Check the borders of the map
    if loc.x <= 0 {
        return false;
    }
    if loc.x >= (p.width - 1) {
        return false;
    }
    if loc.y <= 0 {
        if loc.x == 1 {
            // start - this must be a valid location for moving to,
            // in order to support part 2's requirements
            return true;
        } else {
            return false;
        }
    }
    if loc.y >= (p.height - 1) {
        if loc.x == (p.width - 2) {
            // goal
            return true;
        } else {
            return false;
        }
    }
    // Check for blizzards
    if is_in_blizzard(p, &bms.north, &Vector { dx: 0, dy: -1 }, loc)
    || is_in_blizzard(p, &bms.south, &Vector { dx: 0, dy: 1 },  loc)
    || is_in_blizzard(p, &bms.east,  &Vector { dx: 1, dy: 0 },  loc)
    || is_in_blizzard(p, &bms.west,  &Vector { dx: -1, dy: 0 }, loc) {
        return false;
    }

    // Open space
    return true;
}

#[allow(dead_code)]
fn print_map(p: &Problem, bms: &BlizzardMaps, t: Time) {
    for y in 0 .. p.height {
        for x in 0 .. p.width {
            if can_move_to(p, bms, &Location3D { x: x, y: y, t: t }) {
                print!(".");
            } else {
                print!("#");
            }
        }
        println!();
    }
}

fn find_path(p: &Problem, bms: &BlizzardMaps,
             start: &Location3D, finish: &Location) -> Time {
    let mut todo: BinaryHeap<HeapItem> = BinaryHeap::new();
    let mut planned: HashSet<Location3D> = HashSet::new();

    todo.push(HeapItem {
        loc: *start,
        goal: *finish,
    });
    while !todo.is_empty() {
        let here = todo.pop().unwrap().loc;

        if (here.x == finish.x) && (here.y == finish.y) {
            // goal reached
            return here.t;
        }
        for v in [Vector { dx: 1, dy: 0 },
                  Vector { dx: -1, dy: 0 },
                  Vector { dx: 0, dy: 1 },
                  Vector { dx: 0, dy: -1 },
                  Vector { dx: 0, dy: 0 }] {
            let there = Location3D {
                x: here.x + (v.dx as Word),
                y: here.y + (v.dy as Word),
                t: here.t + 1,
            };
            if !planned.contains(&there)
            && can_move_to(&p, &bms, &there) {
                todo.push(HeapItem {
                    loc: there,
                    goal: *finish,
                });
                planned.insert(there);
            }
        }
    }
    panic!(); // no path
}

fn part1(filename: &str) -> Time {
    let p = load(filename);
    let bms = make_blizzard_maps(&p);
    let start = Location3D { x: 1, y: 0, t: 0, };
    let finish = Location { x: p.width - 2, y: p.height - 1 };
    return find_path(&p, &bms, &start, &finish);
}

fn part2(filename: &str) -> Time {
    let p = load(filename);
    let bms = make_blizzard_maps(&p);
    let start1 = Location3D { x: 1, y: 0, t: 0, };
    let finish1 = Location { x: p.width - 2, y: p.height - 1 };
    let t1 = find_path(&p, &bms, &start1, &finish1);

    let start2 = Location3D { x: finish1.x, y: finish1.y, t: t1, };
    let finish2 = Location { x: start1.x, y: start1.y };
    let t2 = find_path(&p, &bms, &start2, &finish2);

    let start3 = Location3D { x: finish2.x, y: finish2.y, t: t2, };
    let finish3 = finish1;
    return find_path(&p, &bms, &start3, &finish3);
}

#[test]
fn test_part1() {
    assert_eq!(part1(&"test"), 18);
}

#[test]
fn test_part2() {
    assert_eq!(part2(&"test"), 54);
}

fn main() {
    println!("{}", part1(&"input"));
    println!("{}", part2(&"input"));
}

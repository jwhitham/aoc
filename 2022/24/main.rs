
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashSet;

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

fn is_in_blizzard(p: &Problem, bm: &BlizzardMap, dir: &Vector, loc: &Location, t: Time) -> bool {
    // The blizzard moves one "dir" per time unit
    let bl = Location {
        x: Word::rem_euclid(-((dir.dx as Word) * (t as Word)) + loc.x - 1, p.width - 2) + 1,
        y: Word::rem_euclid(-((dir.dy as Word) * (t as Word)) + loc.y - 1, p.height - 2) + 1,
    };
    return bm.contains(&bl);
}

fn can_move_to(p: &Problem, bms: &BlizzardMaps, loc: &Location, t: Time) -> bool {
    // Check the borders of the map
    if loc.x <= 0 {
        return false;
    }
    if loc.x >= (p.width - 1) {
        return false;
    }
    if loc.y <= 0 {
        return false;
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
    if is_in_blizzard(p, &bms.north, &Vector { dx: 0, dy: -1 }, loc, t)
    || is_in_blizzard(p, &bms.south, &Vector { dx: 0, dy: 1 },  loc, t)
    || is_in_blizzard(p, &bms.east,  &Vector { dx: 1, dy: 0 },  loc, t)
    || is_in_blizzard(p, &bms.west,  &Vector { dx: -1, dy: 0 }, loc, t) {
        return false;
    }

    // Open space
    return true;
}

fn print_map(p: &Problem, bms: &BlizzardMaps, t: Time) {
    for y in 0 .. p.height {
        for x in 0 .. p.width {
            if can_move_to(p, bms, &Location { x: x, y: y }, t) {
                print!(".");
            } else {
                print!("#");
            }
        }
        println!();
    }
}


fn part1(filename: &str) -> u32 {
    let p = load(filename);
    let bms = make_blizzard_maps(&p);

    print_map(&p, &bms, 0);
    print_map(&p, &bms, 1);
    print_map(&p, &bms, 2);
    print_map(&p, &bms, 3);
    

    return 0;
}


#[test]
fn test_part1() {
    assert_eq!(part1(&"test"), 18);
}

fn main() {
    println!("{}", part1(&"input"));
}

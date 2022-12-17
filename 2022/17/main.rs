
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;
use std::collections::HashMap;


type MoveIsLeft = Vec<bool>;
type Width = u8;
type Height = u32;
type LargeHeight = u64;

const NUM_ROCK_TYPES: usize = 5;
const NUM_PARTS: usize = 5;
const COL_WIDTH: Width = 7;
const TOP_PART: Height = 6;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Location {
    y: Height,
    x: Width,
}

const ROCK_WIDTH: [Width; NUM_ROCK_TYPES] = [4, 3, 3, 1, 2];
const ROCK_PART: [[Location; NUM_PARTS]; NUM_ROCK_TYPES] = [
    [Location { x: 0, y: 0 }, Location { x: 1, y: 0 }, Location { x: 2, y: 0 },
     Location { x: 3, y: 0 }, Location { x: 3, y: 0 },],
    [Location { x: 1, y: 0 }, Location { x: 0, y: 1 }, Location { x: 1, y: 1 },
     Location { x: 2, y: 1 }, Location { x: 1, y: 2 },],
    [Location { x: 0, y: 0 }, Location { x: 1, y: 0 }, Location { x: 2, y: 0 },
     Location { x: 2, y: 1 }, Location { x: 2, y: 2 },],
    [Location { x: 0, y: 0 }, Location { x: 0, y: 1 }, Location { x: 0, y: 2 },
     Location { x: 0, y: 3 }, Location { x: 0, y: 3 },],
    [Location { x: 0, y: 0 }, Location { x: 1, y: 0 }, Location { x: 1, y: 1 },
     Location { x: 0, y: 1 }, Location { x: 0, y: 1 },],
];


type Occupied = HashSet<Location>;

fn load(filename: &str) -> MoveIsLeft {
    let file = File::open(filename).unwrap();
    let mut p: MoveIsLeft = MoveIsLeft::new();
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            for b in line_string.bytes() {
                match b {
                    b'<' => {
                        p.push(true);
                    },
                    b'>' => {
                        p.push(false);
                    },
                    _ => {}
                }
            }
        }
    }
    return p;
}

fn collision_detect(occupied: &Occupied, rock_pos: &Location, rock_type: usize) -> bool {
    for l in ROCK_PART[rock_type] {
        if occupied.contains(&Location {
            x: rock_pos.x + l.x,
            y: rock_pos.y + l.y,
        }) {
            return true;
        }
    }
    return false;
}

fn simulate_rock(rock_type: usize,
                 move_is_left: &MoveIsLeft, occupied: &mut Occupied,
                 top: &mut Height, move_count: &mut usize) {
    let mut rock_pos = Location { x: 2, y: *top + 3 };
    let rock_width: Width = ROCK_WIDTH[rock_type];

    // while rock is falling
    let mut stop = false;
    while !stop {
        // move left or right
        if *move_is_left.get(*move_count % move_is_left.len()).unwrap() {
            if rock_pos.x > 0 {
                rock_pos.x -= 1;
                if collision_detect(&occupied, &rock_pos, rock_type) {
                    rock_pos.x += 1;
                }
            }
        } else {
            if (rock_pos.x + rock_width) < COL_WIDTH {
                rock_pos.x += 1;
                if collision_detect(&occupied, &rock_pos, rock_type) {
                    rock_pos.x -= 1;
                }
            }
        }
        // loop through moves
        *move_count += 1;
        // try to move down
        if rock_pos.y > 0 {
            rock_pos.y -= 1;
            if collision_detect(&occupied, &rock_pos, rock_type) {
                rock_pos.y += 1;
                stop = true;
            }
        } else {
            stop = true;
        }
    }

    // freeze in place
    assert!(!collision_detect(&occupied, &rock_pos, rock_type));
    for l in ROCK_PART[rock_type] {
        let l2 = Location {
            x: rock_pos.x + l.x,
            y: rock_pos.y + l.y,
        };
        occupied.insert(l2);
        *top = Height::max(*top, rock_pos.y + l.y + 1);
    }
}

fn part1(filename: &str) -> Height {
    let move_is_left = load(filename);
    let mut occupied: Occupied = Occupied::new();
    let mut top: Height = 0;
    let mut move_count: usize = 0;

    // for each rock
    for rock_number in 0 .. 2022 {
        let rock_type: usize = rock_number % NUM_ROCK_TYPES;
        simulate_rock(rock_type, &move_is_left, &mut occupied, &mut top, &mut move_count);
    }
    return top;
}


#[test]
fn test_part1() {
    assert_eq!(part1("test"), 3068);
    assert_eq!(part1("input"), 3067);
}

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct TowerState {
    occupied: u64,
    move_count: usize,
    rock_type: usize,
}

#[derive(Copy, Clone)]
struct TopState {
    rock_number: u64,
    top: Height,
}

fn part2(filename: &str) -> LargeHeight {
    let move_is_left = load(filename);
    let mut occupied: Occupied = Occupied::new();
    let mut top: Height = 0;
    let mut move_count: usize = 0;
    let mut rock_number: u64 = 0;

    // "warm up" - fill at least TOP_PART rows
    while top <= TOP_PART {
        let rock_type: usize = (rock_number as usize) % NUM_ROCK_TYPES;
        simulate_rock(rock_type, &move_is_left, &mut occupied, &mut top, &mut move_count);
        rock_number += 1;
    }

    // now get the period of the simulation by capturing the state of the top part of the tower
    let mut seen: HashMap<TowerState, TopState> = HashMap::new();
    let mut previous: Option<TopState> = None;
    while previous.is_none() {
        let rock_type: usize = (rock_number as usize) % NUM_ROCK_TYPES;
        simulate_rock(rock_type, &move_is_left, &mut occupied, &mut top, &mut move_count);
        rock_number += 1;

        let mut tower_state = TowerState {
            occupied: 0,
            rock_type: rock_type,
            move_count: move_count % move_is_left.len(),
        };
        for y in 0 .. TOP_PART {
            for x in 0 .. COL_WIDTH {
                tower_state.occupied = tower_state.occupied << 1;
                if occupied.contains(&Location { x: x, y: top - 1 - y }) {
                    tower_state.occupied = tower_state.occupied | 1;
                }
            }
        }
        if seen.contains_key(&tower_state) {
            previous = Some(*seen.get(&tower_state).unwrap());
        }
        seen.insert(tower_state, TopState { rock_number: rock_number, top: top });
    }

    // period found
    let rocks_per_period: u64 = rock_number - previous.unwrap().rock_number;
    let rows_per_period: u64 = (top - previous.unwrap().top) as u64;

    // how many more rocks will there be?
    let total_rocks: u64 = 1000000000000;
    let rocks_left: u64 = total_rocks - rock_number;
    let repeats_added: u64 = rocks_left / rocks_per_period;
    rock_number += rocks_per_period * repeats_added;
    assert!(rock_number <= total_rocks);
    assert!(rock_number >= (total_rocks - rocks_per_period - 1));

    // simulate additional rocks to round up
    while rock_number != total_rocks {
        let rock_type: usize = (rock_number % (NUM_ROCK_TYPES as u64)) as usize;
        simulate_rock(rock_type, &move_is_left, &mut occupied, &mut top, &mut move_count);
        rock_number += 1;
    }
    return (top as u64) + (rows_per_period * repeats_added);
}


#[test]
fn test_part2() {
    assert_eq!(part2("test"), 1514285714288);
}

fn main() {
    println!("{}", part1("input"));
    println!("{}", part2("input"));
}



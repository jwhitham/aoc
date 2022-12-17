
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;


type MoveIsLeft = Vec<bool>;
type Height = u16;
type Width = u8;

const NUM_ROCK_TYPES: usize = 5;
const NUM_PARTS: usize = 5;
const COL_WIDTH: Width = 7;

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

fn part1(filename: &str) -> Height {
    let move_is_left = load(filename);
    let mut occupied: Occupied = Occupied::new();
    let mut top: Height = 0;
    let mut move_index: usize = 0;

    // for each rock
    for rock_number in 0 .. 2022 {
        let mut rock_pos = Location { x: 2, y: top + 3 };
        let rock_type: usize = rock_number % NUM_ROCK_TYPES;
        let rock_width: Width = ROCK_WIDTH[rock_type];

        // while rock is falling
        let mut stop = false;
        while !stop {
            // move left or right
            if *move_is_left.get(move_index).unwrap() {
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
            move_index += 1;
            if move_index >= move_is_left.len() {
                move_index = 0;
            }
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
            top = Height::max(top, rock_pos.y + l.y + 1);
        }
    }
    return top;
}


#[test]
fn test_part1() {
    assert_eq!(part1("test"), 3068);
    assert_eq!(part1("input"), 3067);
}

fn main() {
    println!("{}", part1("input"));
}



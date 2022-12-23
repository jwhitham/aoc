
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashMap;

type Word = i16;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Location {
    x: Word,
    y: Word,
}

#[derive(Eq, PartialEq, Copy, Clone)]
struct Elf {
    loc: Location,
    proposed: Option<Location>,
}

type ElfList = Vec<Elf>;

fn load(filename: &str) -> ElfList {
    let file = File::open(filename).unwrap();
    let mut p: ElfList = ElfList::new();
    let mut y: Word = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let bytes = Vec::from_iter(line_string.bytes());
            if bytes.len() == 0 {
                continue;
            }

            let mut x: Word = 0;
            for b in bytes.iter() {
                if *b == b'#' {
                    p.push(Elf {
                        loc: Location { x: x, y: y },
                        proposed: None,
                    });
                }
                x += 1;
            }
            y += 1;
        }
    }
    return p;
}

const NORTH: u32 = 0;
const SOUTH: u32 = 1;
const WEST: u32 = 2;
const EAST: u32 = 3;

#[derive(Eq, PartialEq, Copy, Clone)]
enum Item {
    Empty,
    Occupied,
    ProposedOnce,
    ProposedTwice,
}
    
type ElfMap = HashMap<Location, Item>;

fn get_loc(elf_map: &ElfMap, loc: &Location) -> Item {
    return *elf_map.get(&loc).unwrap_or(&Item::Empty);
}

fn is_occupied(elf_map: &ElfMap, loc: &Location) -> bool {
    return get_loc(elf_map, loc) == Item::Occupied;
}

fn elf_is_lonely(elf: &Elf, elf_map: &ElfMap) -> bool {
    for dy in -1 .. 2 {
        for dx in -1 .. 2 {
            if (dx != 0) || (dy != 0) {
                if is_occupied(elf_map, &Location { x: elf.loc.x + dx, y: elf.loc.y + dy }) {
                    return false;
                }
            }
        }
    }
    return true;
}

fn elf_proposal(elf: &mut Elf, elf_map: &mut ElfMap, direction: u32) -> bool {
    // Is any elf in this direction?
    for d in -1 .. 2 {
        match direction {
            NORTH => {
                if is_occupied(elf_map, &Location { x: elf.loc.x + d, y: elf.loc.y - 1 }) {
                    return false;
                }
            },
            SOUTH => {
                if is_occupied(elf_map, &Location { x: elf.loc.x + d, y: elf.loc.y + 1 }) {
                    return false;
                }
            },
            WEST => {
                if is_occupied(elf_map, &Location { x: elf.loc.x - 1, y: elf.loc.y + d }) {
                    return false;
                }
            },
            EAST => {
                if is_occupied(elf_map, &Location { x: elf.loc.x + 1, y: elf.loc.y + d }) {
                    return false;
                }
            },
            _ => {
                panic!();
            },
        }
    }
    // No elves in the proposed direction - propose a move
    match direction {
        NORTH => {
            elf.proposed = Some(Location { x: elf.loc.x, y: elf.loc.y - 1 });
        },
        SOUTH => {
            elf.proposed = Some(Location { x: elf.loc.x, y: elf.loc.y + 1 });
        },
        WEST => {
            elf.proposed = Some(Location { x: elf.loc.x - 1, y: elf.loc.y });
        },
        EAST => {
            elf.proposed = Some(Location { x: elf.loc.x + 1, y: elf.loc.y });
        },
        _ => {
            panic!();
        },
    }
    match get_loc(elf_map, &elf.proposed.unwrap()) {
        Item::Occupied => {
            panic!();
        },
        Item::Empty => {
            elf_map.insert(elf.proposed.unwrap(), Item::ProposedOnce);
        },
        Item::ProposedOnce | Item::ProposedTwice => {
            elf_map.insert(elf.proposed.unwrap(), Item::ProposedTwice);
        },
    }
    return true;
}

fn elf_move(elf: &mut Elf, elf_map: &mut ElfMap) -> bool {
    if elf.proposed.is_none() {
        // no move
        return false;
    }
    match get_loc(elf_map, &elf.proposed.unwrap()) {
        Item::Occupied | Item::Empty => {
            panic!();
        },
        Item::ProposedOnce => {
            // move
            assert!(is_occupied(elf_map, &elf.loc));
            elf_map.remove(&elf.loc);
            elf.loc = elf.proposed.unwrap();
            return true;
        },
        Item::ProposedTwice => {
            // no move
        },
    }
    return false;
}

fn cleanup(elf: &mut Elf, elf_map: &mut ElfMap) {
    if elf.proposed.is_none() {
        // no cleanup required
        return;
    }
    match get_loc(elf_map, &elf.proposed.unwrap()) {
        Item::Occupied => {
            panic!();
        },
        Item::ProposedOnce => {
            // did move
            elf_map.insert(elf.loc, Item::Occupied);
        },
        Item::ProposedTwice => {
            // didn't move
            elf_map.remove(&elf.proposed.unwrap());
        },
        Item::Empty => {
            // already cleaned up
        },
    }
    elf.proposed = None;
}

fn simulate(filename: &str, part1: bool, limit: u32) -> u32 {

    let mut elf_list = load(filename);
    let mut elf_map: ElfMap = ElfMap::new();

    for elf in elf_list.iter() {
        elf_map.insert(elf.loc, Item::Occupied);
    }

    for round in 0 .. limit as u32 {
        // First part
        for mut elf in elf_list.iter_mut() {
            if !elf_is_lonely(&elf, &elf_map) {
                for offset in 0 .. 4 {
                    if elf_proposal(&mut elf, &mut elf_map, (round + offset) % 4) {
                        break;
                    }
                }
            }
        }
        // Second part
        let mut moved = false;
        for mut elf in elf_list.iter_mut() {
            if elf_move(&mut elf, &mut elf_map) {
                moved = true;
            }
        }
        // Cleanup
        for mut elf in elf_list.iter_mut() {
            cleanup(&mut elf, &mut elf_map);
        }
        // Stop?
        if !moved {
            if !part1 {
                return round + 1;
            }
            break;
        }
    }

    // check that a steady state was reached in part 2
    if !part1 {
        panic!();
    }

    // bounding box
    let mut x1: Word = Word::MAX;
    let mut y1: Word = Word::MAX;
    let mut x2: Word = Word::MIN;
    let mut y2: Word = Word::MIN;
    for elf in elf_list.iter() {
        x1 = Word::min(x1, elf.loc.x);
        x2 = Word::max(x2, elf.loc.x);
        y1 = Word::min(y1, elf.loc.y);
        y2 = Word::max(y2, elf.loc.y);
    }

    let area = ((x2 + 1 - x1) as u32) * ((y2 + 1 - y1) as u32);
    return area - (elf_list.len() as u32);
}

fn part1(filename: &str) -> u32 {
    return simulate(filename, true, 10);
}

fn part2(filename: &str) -> u32 {
    return simulate(filename, false, u32::MAX);
}

#[test]
fn test_part1() {
    assert_eq!(part1(&"test"), 110);
}

#[test]
fn test_part2() {
    assert_eq!(part2(&"test"), 20);
}

fn main() {
    println!("{}", part1(&"input"));
    println!("{}", part2(&"input"));
}

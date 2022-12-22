
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashMap;

const DEBUG: bool = false;
type Word = i16;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Location {
    x: Word,
    y: Word,
}

#[derive(Eq, PartialEq, Copy, Clone)]
enum Item {
    Open,
    Wall,
    Nothing,
}

#[derive(Eq, PartialEq, Copy, Clone)]
enum Move {
    Forward(Word),
    Left,
    Right,
}

#[derive(Eq, PartialEq, Copy, Clone)]
enum Facing {
    North, South, East, West,
}


type World = HashMap<Location, Item>;
type Moves = Vec<Move>;

struct Problem {
    world: World,
    moves: Moves,
    width: Word,
    height: Word,
}


fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p: Problem = Problem {
        world: World::new(),
        moves: Moves::new(),
        width: 0,
        height: 0,
    };
    let mut y: Word = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let bytes = Vec::from_iter(line_string.bytes());
            if bytes.len() == 0 {
                continue;
            }

            match bytes.get(0).unwrap() {
                b' ' | b'.' | b'#' => {
                    parse_line(&mut p, y, &bytes);
                    y += 1;
                },
                _ => {
                    parse_directions(&mut p, &bytes);
                },
            }
        }
    }
    p.height = y;
    return p;
}

fn parse_line(p: &mut Problem, y: Word, bytes: &Vec<u8>) {
    let mut x: Word = 0;
    for b in bytes.iter() {
        p.world.insert(Location {
            x: x,
            y: y,
        }, match b {
            b'.' => Item::Open,
            b'#' => Item::Wall,
            _ => Item::Nothing,
        });
        x += 1;
    }
    p.width = Word::max(x, p.width);
}

fn parse_directions(p: &mut Problem, bytes: &Vec<u8>) {
    let mut number: Word = 0;
    for b in bytes.iter() {
        if (b'0' <= *b) && (*b <= b'9') {
            number *= 10;
            number += (*b - b'0') as Word;
        } else {
            if number != 0 {
                p.moves.push(Move::Forward(number));
                number = 0;
            }
            match b {
                b'L' => {
                    p.moves.push(Move::Left);
                },
                b'R' => {
                    p.moves.push(Move::Right);
                },
                _ => {
                    panic!();
                },
            }
        }
    }
    if number != 0 {
        p.moves.push(Move::Forward(number));
    }
}

fn rotate_left(facing: Facing) -> Facing {
    return match facing {
        Facing::North => Facing::West,
        Facing::West => Facing::South,
        Facing::South => Facing::East,
        Facing::East => Facing::North,
    }
}

fn move_forward(loc: Location, facing: Facing) -> Location {
    let mut loc2 = loc;
    match facing {
        Facing::North => { loc2.y -= 1; },
        Facing::South => { loc2.y += 1; },
        Facing::West =>  { loc2.x -= 1; },
        Facing::East =>  { loc2.x += 1; },
    }
    return loc2;
}

fn get_loc(p: &Problem, loc: &Location) -> Item {
    return *p.world.get(&loc).unwrap_or(&Item::Nothing);
}

fn move_forward_and_wrap(p: &Problem, loc: Location, facing: Facing) -> Location {
    let mut loc2 = move_forward(loc, facing);
    if get_loc(p, &loc2) == Item::Nothing {
        // step into nothingness - wrap around
        match facing {
            Facing::North => { loc2.y = p.height - 1; },
            Facing::South => { loc2.y = 0; },
            Facing::West =>  { loc2.x = p.width - 1; },
            Facing::East =>  { loc2.x = 0; },
        }
        while get_loc(p, &loc2) == Item::Nothing {
            loc2 = move_forward(loc2, facing);
        }
    }
    match get_loc(p, &loc2) {
        Item::Open => {
            // accept
            return loc2;
        },
        Item::Wall => {
            // hit a wall - nothing happens
            return loc;
        },
        Item::Nothing => {
            // Should be impossible
            panic!();
        }
    }
}


fn part1(filename: &str) -> u64 {
    let p = load(filename);
    let mut loc = Location { x: 0, y: 0 };

    // find the start point
    let mut found = false;
    for x in 0 .. p.width {
        loc.x = x;
        if get_loc(&p, &loc) == Item::Open {
            found = true;
            break;
        }
    }
    assert!(found);

    // follow directions
    let mut facing = Facing::East;
    let mut trace: HashMap<Location, Facing> = HashMap::new();

    for d in &p.moves {
        match d {
            Move::Left => {
                facing = rotate_left(facing);
            },
            Move::Right => {
                for _ in 0 .. 3 {
                    facing = rotate_left(facing);
                }
            },
            Move::Forward(n) => {
                for _ in 0 .. *n {
                    trace.insert(loc, facing);
                    loc = move_forward_and_wrap(&p, loc, facing);
                }
            },
        }
    }
    trace.insert(loc, facing);

    // Where do we end up?
    let mut result = (1000 * (1 + (loc.y as u64))) + (4 * (1 + (loc.x as u64)));
    match facing {
        Facing::East =>  { result += 0; },
        Facing::South => { result += 1; },
        Facing::West =>  { result += 2; },
        Facing::North => { result += 3; },
    }

    // Draw it
    if DEBUG {
        for y in 0 .. p.height {
            for x in 0 .. p.width {
                let loc = Location { x: x, y: y };
                let t = trace.get(&loc);
                let item = get_loc(&p, &loc);
                if t.is_some() {
                    assert!(item == Item::Open);
                    match t.unwrap() {
                        Facing::East =>  { print!(">"); },
                        Facing::South => { print!("v"); },
                        Facing::West =>  { print!("<"); },
                        Facing::North => { print!("^"); },
                    }
                } else {
                    match item {
                        Item::Open =>    { print!("."); },
                        Item::Wall =>    { print!("#"); },
                        Item::Nothing => { print!(" "); },
                    }
                }
            }
            println!();
        }
    }
    return result;
}

#[test]
fn test_part1() {
    assert_eq!(part1(&"test"), 6032);
}

fn main() {
    println!("{}", part1(&"input"));
}

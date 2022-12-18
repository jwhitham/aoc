
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;
use std::collections::BinaryHeap;
use std::cmp::Ordering;


type Word = i32;
type Memory = HashMap<Word, Word>;
type InputOutput = Vec<Word>;

struct MachineState {
    memory: Memory,
    input: InputOutput,
    output: InputOutput,
    pc: Word,
    relative_base: Word,
}

fn load_from_input(filename: &str) -> MachineState {
    let file = File::open(filename).unwrap();
    let line = io::BufReader::new(file).lines().next().expect("line").unwrap();
    return load(line.as_str());
}

fn load(line: &str) -> MachineState {
    let mut memory: Memory = HashMap::new();
    let mut index: Word = 0;
    for code in line.split(",") {
        let trimmed = code.trim();
        let parsed: Word = trimmed.parse().expect("number");
        memory.insert(index, parsed);
        index += 1;
    }
    return MachineState {
        memory: memory,
        input: Vec::new(),
        output: Vec::new(),
        pc: 0,
        relative_base: 0,
    };
}

fn get_parameter_mode(opcode: Word, index: Word) -> Word {
    assert!(index >= 1);
    let mut copy = opcode / 100;
    for _ in 1 .. index {
        copy = copy / 10;
    }
    return copy % 10;
}

fn load_memory(ms: &mut MachineState, address: Word) -> Word {
    return *ms.memory.get(&address).unwrap_or(&0);
}

fn store_memory(ms: &mut MachineState, address: Word, value: Word) {
    ms.memory.insert(address, value);
}

fn load_parameter(ms: &mut MachineState, index: Word) -> Word {
    assert!(index >= 1);
    let opcode = load_memory(ms, ms.pc);
    let parameter = load_memory(ms, ms.pc + index);

    return match get_parameter_mode(opcode, index) {
        0 => load_memory(ms, parameter),
        1 => parameter,
        2 => load_memory(ms, parameter + ms.relative_base),
        _ => panic!(),
    }
}

fn store_parameter(ms: &mut MachineState, index: Word, value: Word) {
    assert!(index >= 1);
    let opcode = load_memory(ms, ms.pc);
    let parameter = load_memory(ms, ms.pc + index);

    match get_parameter_mode(opcode, index) {
        0 => store_memory(ms, parameter, value),
        1 => panic!(),
        2 => store_memory(ms, parameter + ms.relative_base, value),
        _ => panic!(),
    }
}

fn run(ms: &mut MachineState) -> Option<Word> {
    loop {
        let opcode = load_memory(ms, ms.pc);
        let a = load_parameter(ms, 1);
        let b = load_parameter(ms, 2);
        match opcode % 100 {
            1 => {
                store_parameter(ms, 3, a + b);
                ms.pc += 4;
            },
            2 => {
                store_parameter(ms, 3, a * b);
                ms.pc += 4;
            },
            3 => {
                if ms.input.is_empty() {
                    return None;
                }
                let v = ms.input.pop().unwrap_or(0);
                store_parameter(ms, 1, v);
                ms.pc += 2;
            },
            4 => {
                ms.pc += 2;
                ms.output.push(a);
            },
            5 => {
                ms.pc += 3;
                if a != 0 {
                    ms.pc = b;
                }
            },
            6 => {
                ms.pc += 3;
                if a == 0 {
                    ms.pc = b;
                }
            },
            7 => {
                if a < b {
                    store_parameter(ms, 3, 1);
                } else {
                    store_parameter(ms, 3, 0);
                }
                ms.pc += 4;
            },
            8 => {
                if a == b {
                    store_parameter(ms, 3, 1);
                } else {
                    store_parameter(ms, 3, 0);
                }
                ms.pc += 4;
            },
            9 => {
                ms.relative_base += a;
                ms.pc += 2;
            },
            99 => {
                return Some(load_memory(ms, 0));
            },
            _ => {
                println!("illegal instruction {} at {}", opcode, ms.pc);
                panic!();
            }
        }
    }
}

#[derive(Eq, PartialEq, Hash, Copy, Clone)]
struct Location {
    x: Word,
    y: Word,
}

#[derive(Eq, PartialEq, Copy, Clone)]
enum Here {
    Hallway,
    Wall,
    Oxygen,
    Unexplored,
    Start,
}

type Maze = HashMap<Location, Here>;

#[derive(Eq, PartialEq, Copy, Clone)]
enum Direction {
    North, South, East, West, Invalid,
}

#[derive(Copy, Clone)]
struct Waypoint {
    from_loc: Location,
    to_loc: Location,
    dir: Direction,
    distance: Word,
}

impl Eq for Waypoint {}

impl PartialEq for Waypoint {
    fn eq(&self, other: &Self) -> bool {
        return self.cmp(other) == Ordering::Equal;
    }
}

impl PartialOrd for Waypoint {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        return Some(self.cmp(other));
    }
}

impl Ord for Waypoint {
    fn cmp(&self, other: &Self) -> Ordering {
        // Need a min-heap so the order is reversed
        if self.distance > other.distance {
            return Ordering::Less;
        } else if self.distance < other.distance {
            return Ordering::Greater;
        } else {
            return Ordering::Equal;
        }
    }
}


fn print_maze(maze: &Maze) {
    let mut left: Word = Word::MAX;
    let mut top: Word = Word::MAX;
    let mut right: Word = Word::MIN;
    let mut bottom: Word = Word::MIN;
    for k in maze.keys() {
        right = Word::max(k.x, right);
        bottom = Word::max(k.y, bottom);
        left = Word::min(k.x, left);
        top = Word::min(k.y, top);
    }
    for y in top .. bottom + 1 {
        for x in left .. right + 1 {
            let loc = Location { x: x, y: y };
            let v = *maze.get(&loc).unwrap_or(&Here::Unexplored);
            match v {
                Here::Hallway =>    { print!("."); },
                Here::Oxygen =>     { print!("o"); },
                Here::Unexplored => { print!("?"); },
                Here::Start =>      { print!("<"); },
                Here::Wall =>       { print!("#"); },
            }
        }
        println!();
    }
}

fn make_route(maze: &Maze, start: &Location, finish: &Location) -> Vec<Waypoint> {
    // Solve shortest-path problem from start to finish
    let mut todo: BinaryHeap<Waypoint> = BinaryHeap::new();
    todo.push(Waypoint {
        from_loc: *start,
        to_loc: *start,
        distance: 0,
        dir: Direction::Invalid,
    });
    let mut done: HashMap<Location, Waypoint> = HashMap::new();

    loop {
        assert!(!todo.is_empty());
        let way: Waypoint = todo.pop().unwrap();

        if done.contains_key(&way.to_loc) {
            // already found a shorter path here
            continue;
        }

        // Shortest path found to this location
        done.insert(way.to_loc, way.clone());

        if way.to_loc == *finish {
            // Found the shortest path
            break;
        }

        // Look for other paths
        let mut add_path = |dx: Word, dy: Word, dir: Direction| {
            let to_loc = Location {
                x: way.to_loc.x + dx,
                y: way.to_loc.y + dy,
            };
            match *maze.get(&to_loc).unwrap_or(&Here::Unexplored) {
                Here::Wall | Here::Unexplored => {
                    // Can't go this way unless it's the end!
                    if to_loc != *finish {
                        return;
                    }
                },
                Here::Oxygen | Here::Hallway | Here::Start => {},
            }
            todo.push(Waypoint {
                from_loc: way.to_loc,
                to_loc: to_loc,
                dir: dir,
                distance: way.distance + 1,
            });
        };
        add_path(-1, 0, Direction::West);
        add_path( 1, 0, Direction::East);
        add_path(0, -1, Direction::North);
        add_path(0,  1, Direction::South);
    }

    // Reconstruct the route from start to finish
    let mut route: Vec<Waypoint> = Vec::new();
    let mut loc = *finish;

    while loc != *start {
        // Push the direction for way.from_loc to way.to_loc
        let way: Waypoint = *done.get(&loc).unwrap();
        loc = way.from_loc;
        route.push(way);
    }
    route.reverse();
    return route;
}

fn part1() {
    let mut ms: MachineState = load_from_input("input");
    let mut maze: Maze = Maze::new();
    let mut stack: Vec<Location> = Vec::new();
    let mut droid = Location { x: 0, y: 0 };
    let mut oxygen: Option<Location> = None;

    maze.insert(Location { x: 0, y: 0 }, Here::Start);
    stack.push(Location { x: 1, y: 0 });
    stack.push(Location { x: -1, y: 0 });
    stack.push(Location { x: 0, y: 1 });
    stack.push(Location { x: 0, y: -1 });

    while !stack.is_empty() {
        let next_unexplored: Location = stack.pop().unwrap();

        if *maze.get(&next_unexplored).unwrap_or(&Here::Unexplored) != Here::Unexplored {
            // Already explored
            continue;
        }
        assert!(next_unexplored != droid);

        // Find a route to the unexplored place and go there
        let route = make_route(&maze, &droid, &next_unexplored);
        assert!(!route.is_empty());
        let mut result: Word = -1;
        for i in 0 .. route.len() {
            assert!(ms.input.is_empty());
            let mv: &Waypoint = route.get(i).unwrap();

            ms.input.push(match mv.dir {
                Direction::North => 1,
                Direction::South => 2,
                Direction::West => 3,
                Direction::East => 4,
                _ => { panic!(); },
            });
            let rc = run(&mut ms);
            assert!(rc.is_none());
            assert!(ms.output.len() == 1);
            result = ms.output.pop().unwrap();
            match result {
                0 => {
                    // Hit a wall - this must be the final move
                    assert!(i == (route.len() - 1));
                },
                1 | 2 => {
                    // Some space here
                },
                _ => {
                    panic!();
                },
            }
        }
        assert!(route.last().unwrap().to_loc == next_unexplored);
        match result {
            0 => {
                // Unexplored space is a wall - droid didn't move
                maze.insert(next_unexplored, Here::Wall);
                droid = route.last().unwrap().from_loc;
            },
            1 => {
                // Unexplored space is hallway
                maze.insert(next_unexplored, Here::Hallway);
                droid = next_unexplored;
            },
            2 => {
                // Unexplored space is an oxygen generator
                maze.insert(next_unexplored, Here::Oxygen);
                droid = next_unexplored;
                oxygen = Some(next_unexplored);
            },
            _ => {
                panic!();
            },
        }
        match result {
            0 => {},
            1 | 2 => {
                // Explore further
                let mut explore = |dx: Word, dy: Word| {
                    let to_loc = Location {
                        x: droid.x + dx,
                        y: droid.y + dy,
                    };
                    if *maze.get(&to_loc).unwrap_or(&Here::Unexplored) == Here::Unexplored {
                        stack.push(to_loc);
                    }
                };
                explore( 1, 0);
                explore(-1, 0);
                explore(0,  1);
                explore(0, -1);
            },
            _ => {
                panic!();
            },
        }
    }
    // Maze is now fully explored!
    assert!(oxygen.is_some());
    let oxy_route = make_route(&maze, &Location { x: 0, y: 0 }, &oxygen.unwrap());
    print_maze(&maze);
    println!("{}", oxy_route.len());
}


fn main() {
    part1();
}


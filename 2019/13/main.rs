
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;

const DEBUG: bool = false;

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

type Screen = HashMap<Location, Word>;

const EMPTY: Word = 0;
const WALL: Word = 1;
const BLOCK: Word = 2;
const PADDLE: Word = 3;
const BALL: Word = 4;


fn print_screen(screen: &Screen) {
    let mut right: Word = 0;
    let mut bottom: Word = 0;
    for k in screen.keys() {
        right = Word::max(k.x, right);
        bottom = Word::max(k.y, bottom);
    }
    for y in 0 .. bottom + 1 {
        for x in 0 .. right + 1 {
            let loc = Location { x: x, y: y };
            let v = *screen.get(&loc).unwrap_or(&0);
            match v {
                EMPTY =>  { print!(" "); },
                WALL =>   { print!("W"); },
                BLOCK =>  { print!("b"); },
                PADDLE => { print!("p"); },
                BALL =>   { print!("0"); },
                _ =>      { print!("?"); },
            }
        }
        println!();
    }
}

fn update_screen(screen: &mut Screen, ms: &mut MachineState) {
    assert_eq!(ms.output.len() % 3, 0);
    for i in 0 .. (ms.output.len() / 3) {
        let j = i * 3;
        let loc = Location {
            x: *ms.output.get(j + 0).unwrap(),
            y: *ms.output.get(j + 1).unwrap(),
        };
        screen.insert(loc, *ms.output.get(j + 2).unwrap());
    }
    ms.output.clear();
}

fn part1() -> usize {
    let mut ms: MachineState = load_from_input("input");

    let rc = run(&mut ms);
    assert!(rc.is_some());

    let mut screen: Screen = HashMap::new();
    update_screen(&mut screen, &mut ms);

    let mut count = 0;
    for v in screen.values() {
        if *v == 2 {
            count += 1;
        }
    }
    if DEBUG {
        print_screen(&screen);
    }
    return count;
}

fn find_item(screen: &Screen, item: Word) -> Location {
    let mut found: Option<Location> = None;
    for (loc, v) in screen {
        if (*v == item) && (loc.x >= 0) && (loc.y >= 0) {
            assert!(found.is_none());
            found = Some(*loc);
        }
    }
    assert!(found.is_some());
    return found.unwrap();
}

fn part2() -> Word {
    let mut ms: MachineState = load_from_input("input");
    let mut screen: Screen = HashMap::new();

    // free play:
    ms.memory.insert(0, 2);

    while run(&mut ms).is_none() {
        assert!(ms.input.is_empty());
        update_screen(&mut screen, &mut ms);

        let ball = find_item(&screen, BALL);
        let paddle = find_item(&screen, PADDLE);

        if paddle.x > ball.x {
            // move left
            ms.input.push(-1);
        } else if paddle.x < ball.x {
            // move right
            ms.input.push(1);
        } else {
            // don't move
            ms.input.push(0);
        }
    }

    // final update
    update_screen(&mut screen, &mut ms);
    if DEBUG {
        print_screen(&screen);
    }
    return *screen.get(&Location { x: -1, y: 0 }).unwrap_or(&0);
}


fn main() {
    println!("{}", part1());
    println!("{}", part2());
}



use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;


type Word = i64;
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

fn part1(filename: &str) -> usize {
    let mut ms: MachineState = load_from_input(filename);
    let mut painted: HashMap<Location, Word> = HashMap::new();
    let mut loc = Location { x: 0, y: 0 };
    let mut dir = 0;

    loop {
        ms.input.push(*painted.get(&loc).unwrap_or(&0));
        let rc = run(&mut ms);
        let second_out = ms.output.pop(); 
        let first_out = ms.output.pop(); 
        assert!(!first_out.is_none());
        assert!(!second_out.is_none());
        assert!((first_out.unwrap() == 0) || (first_out.unwrap() == 1));
        painted.insert(loc, first_out.unwrap());
        match second_out.unwrap() {
            0 => { dir = (dir + 3) % 4; }, // left 90
            1 => { dir = (dir + 1) % 4; }, // right 90
            _ => { panic!(); },
        }
        assert!(ms.output.is_empty());
        assert!(ms.input.is_empty());
        match dir {
            0 => { loc.y -= 1; },
            1 => { loc.x += 1; },
            2 => { loc.y += 1; },
            3 => { loc.x -= 1; },
            _ => panic!(),
        }
        if rc.is_some() {
            break;
        }
    }
    return painted.len();
}


fn main() {
    println!("{}", part1("input"));
}


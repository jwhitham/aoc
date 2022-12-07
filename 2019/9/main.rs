
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;


type Memory = HashMap<i64, i64>;
type InputOutput = Vec<i64>;

struct MachineState {
    memory: Memory,
    input: Vec<i64>,
    output: Vec<i64>,
    pc: i64,
    relative_base: i64,
}

fn load_from_input() -> MachineState {
    let file = File::open("input").unwrap();
    let line = io::BufReader::new(file).lines().next().expect("line").unwrap();
    return load(line.as_str());
}

fn load(line: &str) -> MachineState {
    let mut memory: Memory = HashMap::new();
    let mut index: i64 = 0;
    for code in line.split(",") {
        let trimmed = code.trim();
        let parsed: i64 = trimmed.parse().expect("number");
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

fn get_parameter_mode(opcode: i64, index: i64) -> i64 {
    assert!(index >= 1);
    let mut copy = opcode / 100;
    for _ in 1 .. index {
        copy = copy / 10;
    }
    return copy % 10;
}

fn load_memory(ms: &mut MachineState, address: i64) -> i64 {
    return *ms.memory.get(&address).unwrap_or(&0);
}

fn store_memory(ms: &mut MachineState, address: i64, value: i64) {
    ms.memory.insert(address, value);
}

fn load_parameter(ms: &mut MachineState, index: i64) -> i64 {
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

fn store_parameter(ms: &mut MachineState, index: i64, value: i64) {
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

fn run(ms: &mut MachineState) -> Option<i64> {
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

fn part1() {
    let mut ms: MachineState = load_from_input();
    ms.input.push(1);
    let rc = run(&mut ms);
    assert!(rc.is_some());
    for v in &ms.output {
        println!("{}", v);
    }
    assert_eq!(ms.output.len(), 1);
}


fn main() {
    part1();
}


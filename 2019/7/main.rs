
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;


type Memory = HashMap<i32, i32>;
type InputOutput = Vec<i32>;

fn load_from_input() -> Memory {
    let file = File::open("input").unwrap();
    let line = io::BufReader::new(file).lines().next().expect("line").unwrap();
    return load(line.as_str());
}

fn load(line: &str) -> Memory {
    let mut memory: Memory = HashMap::new();
    let mut index: i32 = 0;
    for code in line.split(",") {
        let trimmed = code.trim();
        let parsed: i32 = trimmed.parse().expect("number");
        memory.insert(index, parsed);
        index += 1;
    }
    return memory;
}

fn get_parameter_mode(opcode: i32, index: i32) -> i32 {
    assert!(index >= 1);
    let mut copy = opcode / 100;
    for _ in 1 .. index {
        copy = copy / 10;
    }
    return copy % 10;
}

fn load_memory(memory: &mut Memory, address: i32) -> i32 {
    return *memory.get(&address).unwrap_or(&0);
}

fn load_parameter(memory: &mut Memory, pc: i32, index: i32) -> i32 {
    assert!(index >= 1);
    let opcode = load_memory(memory, pc);
    let parameter = load_memory(memory, pc + index);

    return match get_parameter_mode(opcode, index) {
        0 => load_memory(memory, parameter),
        1 => parameter,
        _ => panic!(),
    }
}

fn run(memory: &mut Memory, input: &mut InputOutput,
       output: &mut InputOutput) -> i32 {
    let mut pc: i32 = 0;
    loop {
        let opcode = *memory.get(&pc).unwrap_or(&0);
        let a = load_parameter(memory, pc, 1);
        let b = load_parameter(memory, pc, 2);
        match opcode % 100 {
            1 => {
                let r = load_memory(memory, pc + 3);
                pc += 4;
                memory.insert(r, a + b);
            },
            2 => {
                let r = load_memory(memory, pc + 3);
                pc += 4;
                memory.insert(r, a * b);
            },
            3 => {
                let r = load_memory(memory, pc + 1);
                pc += 2;
                memory.insert(r, input.pop().unwrap_or(0));
            },
            4 => {
                pc += 2;
                output.push(a);
            },
            5 => {
                pc += 3;
                if a != 0 {
                    pc = b;
                }
            },
            6 => {
                pc += 3;
                if a == 0 {
                    pc = b;
                }
            },
            7 => {
                let r = load_memory(memory, pc + 3);
                if a < b {
                    memory.insert(r, 1);
                } else {
                    memory.insert(r, 0);
                }
                pc += 4;
            },
            8 => {
                let r = load_memory(memory, pc + 3);
                if a == b {
                    memory.insert(r, 1);
                } else {
                    memory.insert(r, 0);
                }
                pc += 4;
            },
            99 => {
                return load_memory(memory, 0);
            },
            _ => {
                println!("illegal instruction {} at {}", opcode, pc);
                panic!();
            }
        }
    }
}


const NUM_PHASE_SETTINGS: usize = 5;
const NUM_AMPLIFIERS: u8 = 5;

struct State {
    input: InputOutput,
    output: InputOutput,
    initial_memory: Memory,
    carry: i32,
    max_thrust: i32,
    phases_used: [bool; NUM_PHASE_SETTINGS],
    depth: u8,
}

fn part1_solve(state: &mut State) {

    if state.depth >= NUM_AMPLIFIERS {
        state.max_thrust = i32::max(state.max_thrust, state.carry);
        return;
    }


    for i in 0 .. NUM_PHASE_SETTINGS {
        if state.phases_used[i] {
            continue;
        }
        assert!(state.output.is_empty());
        assert!(state.input.is_empty());
        state.input.push(state.carry);
        state.input.push(i as i32);

        let mut memory = state.initial_memory.clone();
        run(&mut memory, &mut state.input, &mut state.output);

        let saved = state.carry;
        state.phases_used[i] = true;
        state.carry = state.output.pop().unwrap();
        state.depth += 1;
        part1_solve(state);
        state.depth -= 1;
        state.carry = saved;
        state.phases_used[i] = false;
    }
}



fn part1() {
    let mut state = State {
        input: Vec::new(),
        output: Vec::new(),
        initial_memory: load_from_input(),
        carry: 0,
        max_thrust: -1,
        phases_used: [false; NUM_PHASE_SETTINGS],
        depth: 0,
    };
    part1_solve(&mut state);
    println!("{}", state.max_thrust);
}

fn main() {
    part1();
}


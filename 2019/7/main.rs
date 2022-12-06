
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
       output: &mut InputOutput, pc: &mut i32) -> Option<i32> {
    loop {
        let opcode = *memory.get(&pc).unwrap_or(&0);
        let a = load_parameter(memory, *pc, 1);
        let b = load_parameter(memory, *pc, 2);
        match opcode % 100 {
            1 => {
                let r = load_memory(memory, *pc + 3);
                *pc += 4;
                memory.insert(r, a + b);
            },
            2 => {
                let r = load_memory(memory, *pc + 3);
                *pc += 4;
                memory.insert(r, a * b);
            },
            3 => {
                if input.is_empty() {
                    return None;
                }
                let r = load_memory(memory, *pc + 1);
                *pc += 2;
                memory.insert(r, input.pop().unwrap_or(0));
            },
            4 => {
                *pc += 2;
                output.push(a);
            },
            5 => {
                *pc += 3;
                if a != 0 {
                    *pc = b;
                }
            },
            6 => {
                *pc += 3;
                if a == 0 {
                    *pc = b;
                }
            },
            7 => {
                let r = load_memory(memory, *pc + 3);
                if a < b {
                    memory.insert(r, 1);
                } else {
                    memory.insert(r, 0);
                }
                *pc += 4;
            },
            8 => {
                let r = load_memory(memory, *pc + 3);
                if a == b {
                    memory.insert(r, 1);
                } else {
                    memory.insert(r, 0);
                }
                *pc += 4;
            },
            99 => {
                return Some(load_memory(memory, 0));
            },
            _ => {
                println!("illegal instruction {} at {}", opcode, *pc);
                panic!();
            }
        }
    }
}


const NUM_PHASE_SETTINGS: usize = 5;
const NUM_AMPLIFIERS: u8 = 5;

struct Part1State {
    input: InputOutput,
    output: InputOutput,
    initial_memory: Memory,
    carry: i32,
    max_thrust: i32,
    phases_used: [bool; NUM_PHASE_SETTINGS],
    depth: u8,
}

fn part1_solve(state: &mut Part1State) {

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
        let mut pc: i32 = 0;
        let rc = run(&mut memory, &mut state.input,
                     &mut state.output, &mut pc);
        assert!(rc.is_some());

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
    let mut state = Part1State {
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

struct Part2State {
    amps: Vec<AmpState>,
    initial_memory: Memory,
    phases_used: [bool; NUM_PHASE_SETTINGS],
    phase_assignment: [i32; NUM_AMPLIFIERS as usize],
    max_thrust: i32,
    depth: u8,
}

struct AmpState {
    input: InputOutput,
    output: InputOutput,
    memory: Memory,
    pc: i32,
    number: usize,
}

fn part2_solve(state: &mut Part2State) {
    // start up each amplifier
    // run to the point where input is expected
    for amp in state.amps.iter_mut() {
        assert!(amp.output.is_empty());
        assert!(amp.input.is_empty());
        amp.memory = state.initial_memory.clone();
        amp.pc = 0;
        amp.input.push(state.phase_assignment[amp.number]);
        let rc = run(&mut amp.memory, &mut amp.input,
                     &mut amp.output, &mut amp.pc);
        assert!(rc.is_none());
        assert!(amp.input.is_empty());
        assert!(amp.output.is_empty());
    }

    let mut feedback: i32 = 0;
    let mut terminated: bool = false;

    while !terminated {
        // iterate to the next amplifier state
        for amp in state.amps.iter_mut() {
            amp.input.push(feedback);
            let rc = run(&mut amp.memory, &mut amp.input,
                         &mut amp.output, &mut amp.pc);
            if amp.number == 0 {
                terminated = rc.is_some();
            } else {
                assert_eq!(terminated, rc.is_some());
            }
            assert!(amp.input.is_empty());
            assert_eq!(amp.output.len(), 1);
            feedback = amp.output.pop().unwrap();
        }
    }

    state.max_thrust = i32::max(state.max_thrust, feedback);
}

fn part2_assign_phases(state: &mut Part2State) {

    if state.depth >= NUM_AMPLIFIERS {
        part2_solve(state);
        return;
    }

    for i in 0 .. NUM_PHASE_SETTINGS {
        if state.phases_used[i] {
            continue;
        }
        state.phases_used[i] = true;
        state.phase_assignment[state.depth as usize] = 5 + i as i32;
        state.depth += 1;
        part2_assign_phases(state);
        state.depth -= 1;
        state.phase_assignment[state.depth as usize] = -1;
        state.phases_used[i] = false;
    }
}

fn part2() {
    let mut state = Part2State {
        amps: Vec::new(),
        initial_memory: load_from_input(),
        max_thrust: -1,
        phases_used: [false; NUM_PHASE_SETTINGS],
        phase_assignment: [-1; NUM_AMPLIFIERS as usize],
        depth: 0,
    };
    for i in 0 .. NUM_AMPLIFIERS {
        state.amps.push(AmpState {
            input: Vec::new(),
            output: Vec::new(),
            memory: HashMap::new(),
            pc: 0,
            number: i as usize,
        });
    }
    part2_assign_phases(&mut state);
    println!("{}", state.max_thrust);
}

fn main() {
    part1();
    part2();
}


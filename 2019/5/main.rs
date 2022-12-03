
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
            99 => {
                return load_memory(memory, 0);
            },
            _ => {
                panic!();
            }
        }
    }
}

#[test]
fn test_old_program() {
    let mut n1: InputOutput = Vec::new();
    let mut n2: InputOutput = Vec::new();
    assert_eq!(run(&mut load("1,9,10,3,2,3,11,0,99,30,40,50"),
                   &mut n1, &mut n2), 3500);
    assert_eq!(run(&mut load("1,0,0,0,99"),
                   &mut n1, &mut n2), 2);
    assert_eq!(run(&mut load("2,3,0,3,99"),
                   &mut n1, &mut n2), 2);
    assert_eq!(run(&mut load("2,4,4,0,99,0"),
                   &mut n1, &mut n2), 9801);
    assert_eq!(run(&mut load("1,1,1,4,99,5,6,0,99"),
                   &mut n1, &mut n2), 30);
}

#[test]
fn test_io_program() {
    let mut n1: InputOutput = Vec::new();
    let mut n2: InputOutput = Vec::new();
    n1.push(123);
    assert_eq!(run(&mut load("3,0,4,0,99"),
                   &mut n1, &mut n2), 123);
    assert!(n1.is_empty());
    assert!(n2.len() == 1);
    assert!(n2.pop().unwrap() == 123);
}

fn part1() -> i32 {
    let mut memory = load_from_input();
    let mut input: InputOutput = Vec::new();
    let mut output: InputOutput = Vec::new();
    input.push(1);
    run(&mut memory, &mut input, &mut output);
    assert!(!output.is_empty());
    return output.pop().unwrap();
}


fn main() {
    let p1 = part1();
    println!("{}", p1);
}


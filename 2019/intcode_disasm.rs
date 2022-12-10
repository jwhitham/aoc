
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;
use std::env;


type Word = i64;
type Memory = HashMap<Word, Word>;

fn load_from_input(filename: &str) -> (Memory, Word) {
    let file = File::open(filename).unwrap();
    let line = io::BufReader::new(file).lines().next().expect("line").unwrap();
    return load(line.as_str());
}

fn load(line: &str) -> (Memory, Word) {
    let mut memory: Memory = HashMap::new();
    let mut index: Word = 0;
    for code in line.split(",") {
        let trimmed = code.trim();
        let parsed: Word = trimmed.parse().expect("number");
        memory.insert(index, parsed);
        index += 1;
    }
    return (memory, index);
}

fn get_parameter_mode(opcode: Word, index: Word) -> Word {
    assert!(index >= 1);
    let mut copy = opcode / 100;
    for _ in 1 .. index {
        copy = copy / 10;
    }
    return copy % 10;
}

fn load_memory(memory: &Memory, address: Word) -> Word {
    return *memory.get(&address).unwrap_or(&0);
}

fn load_parameter(out: &mut String, memory: &Memory, pc: Word, index: Word) {
    let opcode = load_memory(memory, pc);
    let parameter = load_memory(memory, pc + index);

    match get_parameter_mode(opcode, index) {
        0 => {
            out.push_str("[");
            out.push_str(&parameter.to_string());
            out.push_str("]");
        },
        1 => {
            out.push_str(&parameter.to_string());
        },
        2 => {
            out.push_str("[sp");
            if parameter >= 0 {
                out.push_str("+");
            }
            out.push_str(&parameter.to_string());
            out.push_str("]");
        },
        _ => {
            out.push_str("?");
        },
    }
}

fn store_parameter(out: &mut String, memory: &Memory, pc: Word, index: Word) {
    let opcode = load_memory(memory, pc);
    if get_parameter_mode(opcode, index) == 1 {
        out.push_str("?"); // illegal for store
    } else {
        load_parameter(out, memory, pc, index);
    }
}


fn disassemble(memory: &Memory, pc: &mut Word) -> String {
    let opcode = load_memory(memory, *pc);
    let mut out = pc.to_string();
    out.push_str("\t");
    out.push_str(&opcode.to_string());
    out.push_str("\t");
    match opcode % 100 {
        1 => {
            out.push_str("add\t");
            load_parameter(&mut out, memory, *pc, 1);
            out.push_str(" + ");
            load_parameter(&mut out, memory, *pc, 2);
            out.push_str(" -> ");
            store_parameter(&mut out, memory, *pc, 3);
            *pc += 4;
        },
        2 => {
            out.push_str("mul\t");
            load_parameter(&mut out, memory, *pc, 1);
            out.push_str(" * ");
            load_parameter(&mut out, memory, *pc, 2);
            out.push_str(" -> ");
            store_parameter(&mut out, memory, *pc, 3);
            *pc += 4;
        },
        3 => {
            out.push_str("in\tinput -> ");
            store_parameter(&mut out, memory, *pc, 1);
            *pc += 2;
        },
        4 => {
            out.push_str("out\t");
            load_parameter(&mut out, memory, *pc, 1);
            out.push_str(" -> output");
            *pc += 2;
        },
        5 => {
            out.push_str("br\tif ");
            load_parameter(&mut out, memory, *pc, 1);
            out.push_str(" != 0 goto ");
            load_parameter(&mut out, memory, *pc, 2);
            *pc += 3;
        },
        6 => {
            out.push_str("br\tif ");
            load_parameter(&mut out, memory, *pc, 1);
            out.push_str(" == 0 goto ");
            load_parameter(&mut out, memory, *pc, 2);
            *pc += 3;
        },
        7 => {
            out.push_str("cmp\t");
            load_parameter(&mut out, memory, *pc, 1);
            out.push_str(" < ");
            load_parameter(&mut out, memory, *pc, 2);
            out.push_str(" -> ");
            store_parameter(&mut out, memory, *pc, 3);
            *pc += 4;
        },
        8 => {
            out.push_str("cmp\t");
            load_parameter(&mut out, memory, *pc, 1);
            out.push_str(" == ");
            load_parameter(&mut out, memory, *pc, 2);
            out.push_str(" -> ");
            store_parameter(&mut out, memory, *pc, 3);
            *pc += 4;
        },
        9 => {
            out.push_str("adj\tsp + ");
            load_parameter(&mut out, memory, *pc, 1);
            out.push_str(" -> sp");
            *pc += 2;
        },
        99 => {
            out.push_str("halt\t");
            *pc += 1;
        },
        _ => {
            out.push_str("?\t? ");
            out.push_str(&opcode.to_string());
            *pc += 1;
        }
    }
    return out;
}


fn main() -> Result<(), String>{
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        return Err("Provide an intcode file name as a parameter".to_string());
    }
    let (memory, endpoint) = load_from_input(args.get(1).unwrap());
    let mut pc = 0;
    while pc < endpoint {
        println!("{}", disassemble(&memory, &mut pc));
    }
    return Ok(());
}


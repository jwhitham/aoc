
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;


// part 1: 6327510
// part 2: 4112
type Memory = HashMap<i32, i32>;

fn part1() -> i32 {
    let mut memory = load_from_input();
    memory.insert(1, 12);
    memory.insert(2, 2);
    return run(&mut memory);
}

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

fn run(memory: &mut Memory) -> i32 {
    let mut address: i32 = 0;
    loop {
        let opcode = memory.get(&address).unwrap_or(&0);
        let a = *memory.get(&(address + 1)).unwrap_or(&0);
        let b = *memory.get(&(address + 2)).unwrap_or(&0);
        let r = *memory.get(&(address + 3)).unwrap_or(&0);
        match opcode {
            1 => {
                address += 4;
                memory.insert(r, memory.get(&a).unwrap_or(&0)
                                + memory.get(&b).unwrap_or(&0));
            },
            2 => {
                address += 4;
                memory.insert(r, memory.get(&a).unwrap_or(&0)
                                * memory.get(&b).unwrap_or(&0));
            },
            99 => {
                return *memory.get(&0).unwrap_or(&0);
            },
            _ => {
                panic!();
            }
        }
    }
}

#[test]
fn test_part_1() {
    assert_eq!(run(&mut load("1,9,10,3,2,3,11,0,99,30,40,50")), 3500);
    assert_eq!(run(&mut load("1,0,0,0,99")), 2);
    assert_eq!(run(&mut load("2,3,0,3,99")), 2);
    assert_eq!(run(&mut load("2,4,4,0,99,0")), 9801);
    assert_eq!(run(&mut load("1,1,1,4,99,5,6,0,99")), 30);
}

fn part2() -> i32 {
    let initial_memory: Memory = load_from_input();
    for noun in 0 .. 100 {
        for verb in 0 .. 100 {
            let mut memory = initial_memory.clone();
            memory.insert(1, noun);
            memory.insert(2, verb);
            if run(&mut memory) == 19690720 {
                return (100 * noun) + verb;
            }
        }
    }
    panic!();
}


fn main() {
    let p1 = part1();
    println!("{}", p1);
    assert_eq!(p1, 6327510);

    let p2 = part2();
    println!("{}", p2);
    assert_eq!(p2, 4112);
}


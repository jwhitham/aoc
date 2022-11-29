
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::convert::TryInto;

enum Instruction {
    Jio(usize, isize),
    Jie(usize, isize),
    Jmp(isize),
    Inc(usize),
    Tpl(usize),
    Hlf(usize),
}

#[derive(Copy, Clone)]
struct State {
    regs: [usize; 2],
    pc: usize,
}

fn parse_register(name: &str) -> usize {
    if name.starts_with("a") {
        return 0;
    }
    if name.starts_with("b") {
        return 1;
    }
    panic!();
}

fn calc_jump(offset: isize, state: &mut State) {
    let abs_offset: usize = offset.abs().try_into().unwrap();
    state.pc -= 1;
    if offset < 0 {
        if abs_offset > state.pc {
            state.pc = usize::MAX;
        } else {
            state.pc -= abs_offset;
        }
    } else {
        state.pc += abs_offset;
    }
}

fn execute_one(inst: &Instruction, state: &mut State) {
    use Instruction::*;
    state.pc += 1;
    match *inst {
        Jie(reg, offset) => {
            if (state.regs[reg] % 2) == 0 {
                calc_jump(offset, state);
            }
        },
        Jio(reg, offset) => {
            if state.regs[reg] == 1 {
                calc_jump(offset, state);
            }
        },
        Jmp(offset) => {
            calc_jump(offset, state);
        },
        Inc(reg) => {
            state.regs[reg] += 1;
        },
        Hlf(reg) => {
            state.regs[reg] /= 2;
        },
        Tpl(reg) => {
            state.regs[reg] *= 3;
        },
    }
}



fn main() {
    // read program
    let file = File::open("input").unwrap();
    let lines = io::BufReader::new(file).lines();
    let mut program: Vec<Instruction> = Vec::new();
    for line in lines {
        if let Ok(line_string) = line {
            let line_vec = Vec::from_iter(line_string.split_ascii_whitespace());

            assert!(line_vec.len() >= 2);
            use Instruction::*;
            program.push(match line_vec[0] {
                "jio" => Jio(parse_register(line_vec[1]),
                             line_vec[2].parse().unwrap()),
                "jie" => Jie(parse_register(line_vec[1]),
                             line_vec[2].parse().unwrap()),
                "jmp" => Jmp(line_vec[1].parse().unwrap()),
                "inc" => Inc(parse_register(line_vec[1])),
                "tpl" => Tpl(parse_register(line_vec[1])),
                "hlf" => Hlf(parse_register(line_vec[1])),
                _ => panic!(),
            });
        }
    }

    // part 1
    let initial_state = State {
        regs: [0, 0],
        pc: 0,
    };
    let mut state = initial_state;
    while let Some(inst) = program.get(state.pc) {
        execute_one(&inst, &mut state);
    }
    println!("{}", state.regs[parse_register("b")]);

    // part 2
    state = initial_state;
    state.regs[parse_register("a")] = 1;
    while let Some(inst) = program.get(state.pc) {
        execute_one(&inst, &mut state);
    }
    println!("{}", state.regs[parse_register("b")]);
}

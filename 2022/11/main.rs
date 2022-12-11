
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;


type WorryLevel = u32;
type MonkeyNumber = usize;

#[derive(Eq, PartialEq, Copy, Clone)]
enum Opcode {
    Invalid,
    MultiplyConstant,
    Square,
    AddConstant,
}

struct Monkey {
    items: Vec<WorryLevel>,
    opcode: Opcode,
    operand: WorryLevel,
    divisor: WorryLevel,
    true_target: MonkeyNumber,
    false_target: MonkeyNumber,
}

type Island = Vec<Monkey>;

fn load(filename: &str) -> Island {
    let file = File::open(filename).unwrap();
    let mut island: Island = Vec::new();

    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let cleaned = line_string.replace(":", " ")
                                     .replace(",", " ");
            let fields = Vec::from_iter(cleaned.split_ascii_whitespace());

            match *fields.get(0).unwrap_or(&"") {
                "Monkey" => {
                    let m: MonkeyNumber = fields.get(1).unwrap().parse().expect("number");
                    assert_eq!(m, island.len());
                    island.push(Monkey {
                        items: Vec::new(),
                        opcode: Opcode::Invalid,
                        operand: 0,
                        divisor: 1,
                        true_target: 0,
                        false_target: 0,
                    });
                },
                "Starting" => {
                    assert_eq!(*fields.get(1).unwrap(), "items");
                    for i in 2 .. fields.len() {
                        let m: WorryLevel = fields.get(i).unwrap().parse().expect("number");
                        island.last_mut().unwrap().items.push(m);
                    }
                },
                "Operation" => {
                    assert_eq!(*fields.get(1).unwrap(), "new");
                    assert_eq!(*fields.get(2).unwrap(), "=");
                    assert_eq!(*fields.get(3).unwrap(), "old");
                    match *fields.get(4).unwrap() {
                        "+" => {
                            island.last_mut().unwrap().opcode = Opcode::AddConstant;
                            island.last_mut().unwrap().operand =
                                fields.get(5).unwrap().parse().expect("number");
                        },
                        "*" => {
                            if *fields.get(5).unwrap() == "old" {
                                island.last_mut().unwrap().opcode = Opcode::Square;
                            } else {
                                island.last_mut().unwrap().opcode = Opcode::MultiplyConstant;
                                island.last_mut().unwrap().operand =
                                    fields.get(5).unwrap().parse().expect("number");
                            }
                        },
                        _ => {
                            panic!();
                        },
                    }
                },
                "Test" => {
                    assert_eq!(*fields.get(1).unwrap(), "divisible");
                    assert_eq!(*fields.get(2).unwrap(), "by");
                    island.last_mut().unwrap().divisor =
                        fields.get(3).unwrap().parse().expect("number");
                },
                "If" => {
                    match *fields.get(1).unwrap() {
                        "true" => {
                            island.last_mut().unwrap().true_target = fields.get(5).unwrap().parse().expect("number");
                        },
                        "false" => {
                            island.last_mut().unwrap().false_target = fields.get(5).unwrap().parse().expect("number");
                        },
                        _ => {
                            panic!();
                        }
                    }
                },
                "" => {},
                _ => {
                    panic!();
                },
            }
        }
    }
    return island;
}

fn part1(filename: &str) -> usize {
    let mut island = load(filename);

    return island.len();
}

#[test]
fn test_part1() {
    assert_eq!(part1("test10605"), 10605);
}


fn main() {
    println!("{}", part1("input"));
}



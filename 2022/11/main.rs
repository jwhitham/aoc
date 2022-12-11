
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::VecDeque;
use std::cmp::Ordering;


type WorryLevel = u64;
type ActivityLevel = u32;
type MonkeyNumber = usize;

#[derive(Eq, PartialEq, Copy, Clone)]
enum Opcode {
    Invalid,
    MultiplyConstant,
    Square,
    AddConstant,
}

struct Monkey {
    items: VecDeque<WorryLevel>,
    opcode: Opcode,
    operand: WorryLevel,
    divisor: WorryLevel,
    true_target: MonkeyNumber,
    false_target: MonkeyNumber,
    activity: ActivityLevel,
}

impl Eq for Monkey {}

impl PartialEq for Monkey {
    fn eq(&self, other: &Self) -> bool {
        return self.cmp(other) == Ordering::Equal;
    }
}

impl PartialOrd for Monkey {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        return Some(self.cmp(other));
    }
}

impl Ord for Monkey {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.activity < other.activity {
            return Ordering::Less;
        } else if self.activity > other.activity {
            return Ordering::Greater;
        } else {
            return Ordering::Equal;
        }
    }
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
                        items: VecDeque::new(),
                        opcode: Opcode::Invalid,
                        operand: 0,
                        divisor: 1,
                        true_target: 0,
                        false_target: 0,
                        activity: 0,
                    });
                },
                "Starting" => {
                    assert_eq!(*fields.get(1).unwrap(), "items");
                    for i in 2 .. fields.len() {
                        let item: WorryLevel = fields.get(i).unwrap().parse().expect("number");
                        island.last_mut().unwrap().items.push_back(item);
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

fn simulate(filename: &str, num_rounds: usize, divide: bool) -> ActivityLevel {
    let mut island = load(filename);

    // for each round
    for _ in 0 .. num_rounds {
        // for each monkey's turn
        for m1 in 0 .. island.len() {
            let initial_number_of_items = island.get(m1).unwrap().items.len();

            // for each item
            for _ in 0 .. initial_number_of_items {
                // remove item
                let mut item = island.get_mut(m1).unwrap().items.pop_front().unwrap();

                // inspection!
                match island.get(m1).unwrap().opcode {
                    Opcode::AddConstant => {
                        item += island.get(m1).unwrap().operand;
                    },
                    Opcode::MultiplyConstant => {
                        item *= island.get(m1).unwrap().operand;
                    },
                    Opcode::Square => {
                        item *= item;
                    },
                    Opcode::Invalid => {
                        panic!();
                    },
                }
                // count activity
                island.get_mut(m1).unwrap().activity += 1;
                // gets bored
                if divide {
                    item /= 3;
                }
                // where next?
                let mut m2 = island.get(m1).unwrap().true_target;
                if (item % island.get(m1).unwrap().divisor) != 0 {
                    m2 = island.get(m1).unwrap().false_target;
                }
                // throw to new monkey (possibly the same monkey?)
                island.get_mut(m2).unwrap().items.push_back(item);
            }
        }
    }

    // which monkeys are most active?
    island.sort();

    let most_active = island.pop().unwrap().activity;
    let second_most_active = island.pop().unwrap().activity;
    return most_active * second_most_active;
}

fn part1(filename: &str) -> ActivityLevel {
    return simulate(filename, 20, true);
}

fn part2(filename: &str) -> ActivityLevel {
    return simulate(filename, 10000, false);
}

#[test]
fn test_part1() {
    assert_eq!(part1("test10605"), 10605);
}

#[test]
fn test_part2() {
    assert_eq!(part2("test10605"), 2713310158);
}


fn main() {
    println!("{}", part1("input"));
    println!("{}", part2("input"));
}



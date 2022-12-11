
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::VecDeque;
use std::cmp::Ordering;

// Represent the large number Z by an array of small values
//
// div[X] means "Z - div[X] is divisible by X"
// where X is a small prime number [2..19]
// and div[X] is any integer in the range [0..X)
//
// impact of multiplying by a constant:
//
// BEFORE: 79             has div[13] = 1, div[17] = 11, div[19] = 3, div[23] = 10
// AFTER:  79 * 19 = 1501 has div[13] = 6, div[17] = 5,  div[19] = 0, div[23] = 6
//      x  div[x]  * 19   new div[x]   
//      13     1    ->    6 = (1 * 19) % 13
//      17    11    ->    5 = (11 * 19) % 17
//      19     3    ->    0 = (3 * 19) % 19
//      23    10    ->    6 = (10 * 19) % 23
//
// impact of squaring:
//
// BEFORE: 79             has div[13] = 1, div[17] = 11, div[19] = 3, div[23] = 10
// AFTER:  79 * 79 = 6241 has div[13] = 1, div[17] = 2,  div[19] = 9, div[23] = 8
//      x  div[x]  ** 2   new div[x]   
//      13     1    ->    1 = ((1 + 13) ** 2) % 13
//      17    11    ->    2 = ((11 + 17) ** 2) % 17
//      19     3    ->    9 = ((3 + 19) ** 2) % 19
//      23    10    ->    8 = ((10 + 23) ** 2) % 23
//
// impact of adding a constant:
//
// BEFORE: 79             has div[13] = 1, div[17] = 11, div[19] = 3,  div[23] = 10
// AFTER:  79 + 7 = 86    has div[13] = 8, div[17] = 1,  div[19] = 10, div[23] = 17
//      x  div[x]  + 7    new div[x]   
//      13     1    ->    8 = (1 + 7) % 13
//      17    11    ->    1 = (11 + 7) % 17
//      19     3    ->    10 = (3 + 7) % 19
//      23    10    ->    17 = (10 + 7) % 23
//

type Part1WorryLevel = u64;
type Part2WorryLevel = u16;
const PRIME_TABLE_SIZE: usize = 9;
const PRIME_TABLE: [Part2WorryLevel; PRIME_TABLE_SIZE] = [2, 3, 5, 7, 11, 13, 17, 19, 23];
type ActivityLevel = u64;
type MonkeyNumber = usize;

#[derive(Eq, PartialEq, Copy, Clone)]
enum Opcode {
    Invalid,
    MultiplyConstant,
    Square,
    AddConstant,
}

struct WorryLevel {
    part1: Part1WorryLevel,
    div: [Part2WorryLevel; PRIME_TABLE_SIZE],
}

struct Monkey {
    items: VecDeque<WorryLevel>,
    opcode: Opcode,
    operand: Part1WorryLevel,
    divisor: Part1WorryLevel,
    divisor_index: usize,
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

fn convert_worry_level(s: Part1WorryLevel) -> WorryLevel {
    let mut w = WorryLevel {
        div: [0; PRIME_TABLE_SIZE],
        part1: s,
    };
    for i in 0 .. PRIME_TABLE_SIZE {
        w.div[i] = (s as Part2WorryLevel) % PRIME_TABLE[i];
    }
    return w;
}

fn convert_divisor(s: Part1WorryLevel) -> usize {
    for i in 0 .. PRIME_TABLE_SIZE {
        if (s as Part2WorryLevel) == PRIME_TABLE[i] {
            return i;
        }
    }
    panic!();
}

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
                        divisor_index: 0,
                        true_target: 0,
                        false_target: 0,
                        activity: 0,
                    });
                },
                "Starting" => {
                    assert_eq!(*fields.get(1).unwrap(), "items");
                    for i in 2 .. fields.len() {
                        let item: Part1WorryLevel = fields.get(i).unwrap().parse().expect("number");
                        island.last_mut().unwrap().items.push_back(convert_worry_level(item));
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
                    let d: Part1WorryLevel = fields.get(3).unwrap().parse().expect("number");
                    island.last_mut().unwrap().divisor = d;
                    island.last_mut().unwrap().divisor_index = convert_divisor(d);
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

fn simulate(filename: &str, num_rounds: usize, part1: bool) -> ActivityLevel {
    let mut island = load(filename);

    // for each round
    for _ in 0 .. num_rounds {
        // for each monkey's turn
        for m1 in 0 .. island.len() {
            let initial_number_of_items = island.get(m1).unwrap().items.len();
            let opcode = island.get(m1).unwrap().opcode;
            let operand = island.get(m1).unwrap().operand;

            // for each item
            for _ in 0 .. initial_number_of_items {
                // remove item
                let mut item = island.get_mut(m1).unwrap().items.pop_front().unwrap();
                let is_divisible: bool;

                if part1 {
                    // inspection!
                    match opcode {
                        Opcode::AddConstant => {
                            item.part1 += operand;
                        },
                        Opcode::MultiplyConstant => {
                            item.part1 *= operand;
                        },
                        Opcode::Square => {
                            item.part1 *= item.part1;
                        },
                        Opcode::Invalid => {
                            panic!();
                        },
                    }
                    // gets bored
                    item.part1 /= 3;
                    // where next?
                    is_divisible = (item.part1 % island.get(m1).unwrap().divisor) == 0;
                } else {
                    // inspection!
                    match opcode {
                        Opcode::AddConstant => {
                            for i in 0 .. PRIME_TABLE_SIZE {
                                item.div[i] = (item.div[i] + (operand as Part2WorryLevel)) % PRIME_TABLE[i];
                            }
                        },
                        Opcode::MultiplyConstant => {
                            for i in 0 .. PRIME_TABLE_SIZE {
                                item.div[i] = (item.div[i] * (operand as Part2WorryLevel)) % PRIME_TABLE[i];
                            }
                        },
                        Opcode::Square => {
                            for i in 0 .. PRIME_TABLE_SIZE {
                                let v = item.div[i] + PRIME_TABLE[i];
                                item.div[i] = (v * v) % PRIME_TABLE[i];
                            }
                        },
                        Opcode::Invalid => {
                            panic!();
                        },
                    }
                    is_divisible = item.div[island.get(m1).unwrap().divisor_index] == 0;
                }
                // count activity
                island.get_mut(m1).unwrap().activity += 1;
                // where next?
                let mut m2 = island.get(m1).unwrap().true_target;
                if !is_divisible {
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



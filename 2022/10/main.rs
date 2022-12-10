
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;


type Word = i64;
type TraceX = Vec<Word>;

fn part1(filename: &str) -> Word {
    let file = File::open(filename).unwrap();
    let mut trace: TraceX = Vec::new();
    let mut x_register: Word = 1;
    trace.push(x_register); // 0th cycle

    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let words = Vec::from_iter(line_string.split_ascii_whitespace());
            assert!(words.len() >= 1);
            let opcode: &str = *words.get(0).unwrap();
            match opcode {
                "noop" => {
                    assert!(words.len() == 1);
                    trace.push(x_register);
                },
                "addx" => {
                    assert!(words.len() == 2);
                    let value: Word = words.get(1).unwrap().parse().expect("number");
                    trace.push(x_register);
                    trace.push(x_register);
                    x_register += value;
                },
                _ => {
                    panic!();
                },
            }
        }
    }
    let mut examine: usize = 20;
    let mut total: Word = 0;
    while examine < trace.len() {
        total += trace.get(examine).unwrap() * (examine as Word);
        examine += 40;
    }
    return total;
}

#[test]
fn test_part1() {
    assert_eq!(part1("test13140"), 13140);
}

fn main() {
    println!("{}", part1("input"));
}



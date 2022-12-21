
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashMap;

type Word = i64;

#[derive(Clone, Eq, PartialEq)]
enum Op {
    Literal(Word),
    Add(String, String),
    Sub(String, String),
    Div(String, String),
    Mul(String, String),
}

type Problem = HashMap<String, Op>;

fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p: Problem = Problem::new();
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let cleaned = line_string.replace(":", " ");
            let fields = Vec::from_iter(cleaned.split_ascii_whitespace());
            assert!(fields.len() >= 2);
            let name: String = fields.get(0).unwrap().to_string();
            match fields.len() {
                2 => {
                    let v: Word = fields.get(1).unwrap().parse().expect("n");
                    p.insert(name, Op::Literal(v));
                },
                4 => {
                    let a: String = fields.get(1).unwrap().to_string();
                    let b: String = fields.get(3).unwrap().to_string();
                    match *fields.get(2).unwrap() {
                        "+" => {
                            p.insert(name, Op::Add(a, b));
                        },
                        "-" => {
                            p.insert(name, Op::Sub(a, b));
                        },
                        "/" => {
                            p.insert(name, Op::Div(a, b));
                        },
                        "*" => {
                            p.insert(name, Op::Mul(a, b));
                        },
                        _ => {
                            panic!();
                        },
                    }
                },
                _ => {
                    panic!();
                },
            }
        }
    }
    return p;
}

fn calc(p: &Problem, name: &String) -> Word {
    let op: &Op = p.get(name).unwrap();
    match op {
        Op::Literal(v) => {
            return *v;
        },
        Op::Add(a, b) => {
            return calc(p, a) + calc(p, b);
        },
        Op::Mul(a, b) => {
            return calc(p, a) * calc(p, b);
        },
        Op::Div(a, b) => {
            return calc(p, a) / calc(p, b);
        },
        Op::Sub(a, b) => {
            return calc(p, a) - calc(p, b);
        },
    }
}

fn part1(p: &Problem) -> Word {
    return calc(p, &"root".to_string());
}

#[test]
fn test_part1() {
    assert_eq!(part1(&load(&"test")), 152);
}

fn main() {
    println!("{}", part1(&load(&"input")));
}


use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashMap;

type Word = i64;

#[derive(Clone, Eq, PartialEq)]
enum Node {
    Literal(Word),
    Binary(Op, String, String),
}

#[derive(Copy, Clone, Eq, PartialEq)]
enum Op {
    Add,
    Sub,
    Div,
    Mul,
}

type Problem = HashMap<String, Node>;
type Cache = HashMap<String, Word>;

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
                    p.insert(name, Node::Literal(v));
                },
                4 => {
                    let a: String = fields.get(1).unwrap().to_string();
                    let b: String = fields.get(3).unwrap().to_string();
                    match *fields.get(2).unwrap() {
                        "+" => {
                            p.insert(name, Node::Binary(Op::Add, a, b));
                        },
                        "-" => {
                            p.insert(name, Node::Binary(Op::Sub, a, b));
                        },
                        "/" => {
                            p.insert(name, Node::Binary(Op::Div, a, b));
                        },
                        "*" => {
                            p.insert(name, Node::Binary(Op::Mul, a, b));
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

fn calc(p: &Problem, name: &String, cache: &mut Cache) -> Word {
    let cached = cache.get(name);
    if cached.is_some() {
        return *cached.unwrap();
    }
    let node: &Node = p.get(name).unwrap();
    let out: Word;
    match node {
        Node::Literal(v) => {
            out = *v;
        },
        Node::Binary(op, a, b) => {
            match op {
                Op::Add => {
                    out = calc(p, a, cache) + calc(p, b, cache);
                },
                Op::Mul => {
                    out = calc(p, a, cache) * calc(p, b, cache);
                },
                Op::Div => {
                    out = calc(p, a, cache) / calc(p, b, cache);
                },
                Op::Sub => {
                    out = calc(p, a, cache) - calc(p, b, cache);
                },
            }
        },
    }
    cache.insert(name.to_string(), out);
    return out;
}

fn part1(p: &Problem) -> Word {
    return calc(p, &"root".to_string(), &mut Cache::new());
}

#[test]
fn test_part1() {
    assert_eq!(part1(&load(&"test")), 152);
}

fn part2(p: &Problem) -> Word {
    let mut copy = p.clone();
    let match_a: String;
    let match_b: String;
    match copy.get(&"root".to_string()).unwrap() {
        Node::Literal(_) => {
            panic!();
        },
        Node::Binary(_, a, b) => {
            match_a = a.to_string(); match_b = b.to_string();
        },
    }
    copy.remove(&"root".to_string());
    let mut cache_a = Cache::new();
    calc(&copy, &match_a, &mut cache_a);
    let mut cache_b = Cache::new();
    calc(&copy, &match_b, &mut cache_b);
    if cache_a.contains_key(&"humn".to_string()) {
        println!("cache a!");
    }
    if cache_a.contains_key(&"humn".to_string()) {
        println!("cache b!");
    }
    return 0;
}

#[test]
fn test_part2() {
    assert_eq!(part2(&load(&"test")), 301);
}

fn main() {
    println!("{}", part1(&load(&"input")));
    println!("{}", part2(&load(&"input")));
}

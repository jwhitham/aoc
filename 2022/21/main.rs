
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashMap;

type Word = i64;
const DEBUG: bool = false;
const ROOT: &str = "root";
const HUMN: &str = "humn";

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

fn calc(p: &Problem, name: &String, cache: &mut Cache) -> Option<Word> {
    let cached: Option<&Word> = cache.get(name);
    if cached.is_some() {
        return Some(*cached.unwrap());
    }
    let node: Option<&Node> = p.get(name);
    if node.is_none() {
        assert_eq!(name, &HUMN);
        return None;
    }
    let out: Word;
    match node.unwrap() {
        Node::Literal(v) => {
            out = *v;
        },
        Node::Binary(op, a, b) => {
            let av = calc(p, &a, cache);
            if av.is_none() {
                return None;
            }
            let bv = calc(p, &b, cache);
            if bv.is_none() {
                return None;
            }
            match op {
                Op::Add => {
                    out = av.unwrap() + bv.unwrap();
                },
                Op::Mul => {
                    out = av.unwrap() * bv.unwrap();
                },
                Op::Div => {
                    out = av.unwrap() / bv.unwrap();
                },
                Op::Sub => {
                    out = av.unwrap() - bv.unwrap();
                },
            }
        },
    }
    cache.insert(name.to_string(), out);
    return Some(out);
}

fn part1(p: &Problem) -> Word {
    return calc(p, &ROOT.to_string(), &mut Cache::new()).unwrap();
}

#[test]
fn test_part1() {
    assert_eq!(part1(&load(&"test")), 152);
}

fn print_expr(p: &Problem, sub_root: &String) {
    let found = p.get(sub_root);
    if found.is_none() {
        assert_eq!(sub_root, HUMN);
        print!("{}", sub_root);
        return;
    }
    match found.unwrap() {
        Node::Literal(v) => {
            print!("{}", v);
        },
        Node::Binary(op, a, b) => {
            print!("(");
            print_expr(p, a);
            match op {
                Op::Add => { print!(" + "); },
                Op::Sub => { print!(" - "); },
                Op::Mul => { print!(" * "); },
                Op::Div => { print!(" / "); },
            }
            print_expr(p, b);
            print!(")");
        },
    }
}

fn solve(p: &mut Problem, sub_root: &String, cache: &mut Cache,
         equals: Word) -> Word {
    if DEBUG {
        print_expr(p, sub_root);
        println!(" = {}", equals);
    }
    let rn: Option<&Node> = p.get(sub_root);
    if rn.is_none() {
        // Have reached humn = equals
        assert_eq!(sub_root, HUMN);
        return equals;
    }
    match rn.unwrap().clone() {
        Node::Literal(_) => {
            // Must be a binary operation
            panic!();
        },
        Node::Binary(op, ma, mb) => {
            let va = calc(&p, &ma, cache);
            let vb = calc(&p, &mb, cache);
            if va.is_none() && vb.is_none() {
                // Can't solve problems where "humn" appears on both sides
                panic!();
            } else if va.is_some() && vb.is_some() {
                // Can't solve problems where "humn" doesn't appear
                panic!();
            }
            match op {
                Op::Sub => {
                    if va.is_some() {
                        // va - ? = equals
                        // va = ? + equals
                        // va - equals = ?
                        return solve(p, &mb, cache, va.unwrap() - equals);
                    } else {
                        // ? - vb = equals
                        // ? = vb + equals
                        return solve(p, &ma, cache, vb.unwrap() + equals);
                    }
                },
                Op::Div => {
                    if va.is_some() {
                        // va / ? = equals
                        // va / equals = ?
                        return solve(p, &mb, cache, va.unwrap() / equals);
                    } else {
                        // ? / vb = equals
                        // ? = vb * equals
                        return solve(p, &ma, cache, vb.unwrap() * equals);
                    }
                },
                Op::Add => {
                    if va.is_some() {
                        // va + ? = equals
                        return solve(p, &mb, cache, equals - va.unwrap());
                    } else {
                        // ? + vb = equals
                        return solve(p, &ma, cache, equals - vb.unwrap());
                    }
                },
                Op::Mul => {
                    if va.is_some() {
                        // va * ? = equals
                        return solve(p, &mb, cache, equals / va.unwrap());
                    } else {
                        // ? * vb = equals
                        return solve(p, &ma, cache, equals / vb.unwrap());
                    }
                },
            }
        },
    }
}
    
fn part2(p: &mut Problem) -> Word {
    p.remove(&HUMN.to_string());
    match p.remove(&ROOT.to_string()).unwrap() {
        Node::Literal(_) => {
            // Root must be a binary operation
            panic!();
        },
        Node::Binary(_, ma, mb) => {
            // Rewrite root as A - B so that we can solve A - B = 0
            p.insert(ROOT.to_string(), Node::Binary(Op::Sub, ma, mb));
        },
    }
    return solve(p, &ROOT.to_string(), &mut Cache::new(), 0);
}

#[test]
fn test_part2() {
    assert_eq!(part2(&mut load(&"test")), 301);
}

fn main() {
    println!("{}", part1(&load(&"input")));
    println!("{}", part2(&mut load(&"input")));
}

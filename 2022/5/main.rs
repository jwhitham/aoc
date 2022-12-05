
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::VecDeque;
use std::iter::FromIterator;

const NUM_STACKS: usize = 9;

type Stack = VecDeque<char>;
type Stacks = Vec<Stack>;

fn part(part_number: u32) {
    let file = File::open("input").unwrap();

    let mut stacks: Stacks = Vec::new();

    for _ in 0 .. NUM_STACKS {
        stacks.push(VecDeque::new());
    }
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            if !line_string.starts_with("move") {
                let mut col: usize = 0;
                for ch in line_string.chars() {
                    col += 1;
                    if ch >= 'A' && ch <= 'Z' {
                        assert!((col % 4) == 2);
                        assert!((col / 4) < NUM_STACKS);
                        stacks.get_mut(col / 4).unwrap().push_front(ch);
                    }
                }
            } else {
                let words = Vec::from_iter(line_string.split_ascii_whitespace());
                assert!(words.get(2).unwrap().starts_with("from"));
                assert!(words.get(4).unwrap().starts_with("to"));
                let count: usize = words.get(1).unwrap().parse().expect("count");
                let src: usize = words.get(3).unwrap().parse().expect("src");
                let dest: usize = words.get(5).unwrap().parse().expect("dest");

                match part_number {
                    1 => {
                        for _ in 0 .. count {
                            let src_stack: &mut Stack = stacks.get_mut(src - 1).unwrap();
                            let value = src_stack.pop_back().expect("stack");
                            let dest_stack: &mut Stack = stacks.get_mut(dest - 1).unwrap();
                            dest_stack.push_back(value);
                        }
                    },
                    2 => {
                        let mut temp: Vec<char> = Vec::new();
                        for _ in 0 .. count {
                            let src_stack: &mut Stack = stacks.get_mut(src - 1).unwrap();
                            let value = src_stack.pop_back().expect("stack");
                            temp.push(value);
                        }
                        for _ in 0 .. count {
                            let value = temp.pop().unwrap();
                            let dest_stack: &mut Stack = stacks.get_mut(dest - 1).unwrap();
                            dest_stack.push_back(value);
                        }
                    },
                    _ => {
                        panic!();
                    },
                }
            }
        }
    }

    for i in 0 .. NUM_STACKS {
        let src_stack = stacks.get(i).unwrap();
        print!("{}", src_stack.back().unwrap());
    }
    println!("");
}

fn main() {
    part(1);
    part(2);
}


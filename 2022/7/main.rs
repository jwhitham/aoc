
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;
use std::iter::FromIterator;


fn add_to_tree_size(tree_size: &mut HashMap<String, usize>,
                    path: &mut Vec<String>, size: usize) {
    let dir_name: String = path.join("/");
    let new_size: usize = tree_size.get(&dir_name).unwrap_or(&0) + size;

    tree_size.insert(dir_name, new_size);
    if !path.is_empty() {
        let saved = path.pop().unwrap();
        add_to_tree_size(tree_size, path, size);
        path.push(saved);
    }
}

fn part1() {
    let file = File::open("input").unwrap();
    let mut path: Vec<String> = Vec::new();
    let mut tree_size: HashMap<String, usize> = HashMap::new();

    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let trimmed = line_string.trim();
            let line_vec = Vec::from_iter(trimmed.split_ascii_whitespace());

            match *line_vec.get(0).unwrap() {
                "$" => match *line_vec.get(1).unwrap() {
                    "cd" => match *line_vec.get(2).unwrap() {
                        ".." => {
                            path.pop();
                        },
                        "/" => {
                            path.clear();
                        },
                        _ => {
                            path.push(line_vec.get(2).unwrap().to_string());
                        },
                    },
                    "ls" => {},
                    _ => panic!(),
                },
                "dir" => {},
                _ => {
                    let size: usize = line_vec.get(0).unwrap().parse().expect("size");
                    add_to_tree_size(&mut tree_size, &mut path, size);
                },
            }
        }
    }

    let mut total: usize = 0;
    for (_, size) in &tree_size {
        if *size <= 100000 {
            total += *size;
        }
    }
    println!("{}", total);
}

fn main () {
    part1();
}

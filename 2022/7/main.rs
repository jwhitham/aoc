
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

fn main () {
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

    let mut part1_used: usize = 0;
    for size in tree_size.values() {
        if *size <= 100000 {
            part1_used += *size;
        }
    }
    println!("{}", part1_used);

    let disk_size: usize = 70000000;
    let free_space_required: usize = 30000000;
    let total_used: usize = *tree_size.get("").unwrap(); // tree size at the root
    let free_space_available: usize = disk_size - total_used;
    let need_to_delete: usize = free_space_required - free_space_available;
    let mut part2_choice: usize = usize::MAX;

    for size in tree_size.values() {
        if *size >= need_to_delete {
            part2_choice = usize::min(part2_choice, *size);
        }
    }
    println!("{}", part2_choice);
}

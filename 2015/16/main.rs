
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;

/*
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
*/

fn part1() {
    // Read input and do part 1
    let file = File::open("input").unwrap();
    let lines = io::BufReader::new(file).lines();
    for line in lines {
        if let Ok(line_string) = line {
            let decomma = line_string.replace(",", "");
            let decolon = decomma.replace(":", "");
            let line_vec = Vec::from_iter(decolon.split_ascii_whitespace());

            assert_eq!(line_vec[0], "Sue");
            let mut wrong = false;

            for i in 2 .. line_vec.len() - 1 {
                let key = line_vec[i];
                let parsed = line_vec[i + 1].parse();
                if parsed.is_ok() {
                    let value: i32 = parsed.unwrap();
                    if ((key == "children") && (value != 3))
                    || ((key == "cats") && (value != 7))
                    || ((key == "samoyeds") && (value != 2))
                    || ((key == "pomeranians") && (value != 3))
                    || ((key == "akitas") && (value != 0))
                    || ((key == "vizslas") && (value != 0))
                    || ((key == "goldfish") && (value != 5))
                    || ((key == "trees") && (value != 3))
                    || ((key == "cars") && (value != 2))
                    || ((key == "perfumes") && (value != 1)) {
                        wrong = true;
                        break;
                    }
                }
            }

            if !wrong {
                println!("{}", line_vec[1]);
            }
        }
    }
}

fn part2() {
    // Read input and do part 2
    let file = File::open("input").unwrap();
    let lines = io::BufReader::new(file).lines();
    for line in lines {
        if let Ok(line_string) = line {
            let decomma = line_string.replace(",", "");
            let decolon = decomma.replace(":", "");
            let line_vec = Vec::from_iter(decolon.split_ascii_whitespace());

            assert_eq!(line_vec[0], "Sue");
            let mut wrong = false;

            for i in 2 .. line_vec.len() - 1 {
                let key = line_vec[i];
                let parsed = line_vec[i + 1].parse();
                if parsed.is_ok() {
                    let value: i32 = parsed.unwrap();
                    if ((key == "children") && (value != 3))
                    || ((key == "cats") && !(value > 7))
                    || ((key == "samoyeds") && (value != 2))
                    || ((key == "pomeranians") && !(value < 3))
                    || ((key == "akitas") && (value != 0))
                    || ((key == "vizslas") && (value != 0))
                    || ((key == "goldfish") && !(value < 5))
                    || ((key == "trees") && !(value > 3))
                    || ((key == "cars") && (value != 2))
                    || ((key == "perfumes") && (value != 1)) {
                        wrong = true;
                        break;
                    }
                }
            }

            if !wrong {
                println!("{}", line_vec[1]);
            }
        }
    }
}

fn main() {
    part1();
    part2();
}

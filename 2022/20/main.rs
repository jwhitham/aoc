
use std::fs::File;
use std::io::{self, BufRead};

#[derive(Copy, Clone)]
struct Number {
    value: isize,
    order: usize,
}

type Problem = Vec<Number>;

fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p: Problem = Problem::new();
    let mut order: usize = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            p.push(Number {
                value: line_string.parse().expect("n"),
                order: order,
            });
            order += 1;
        }
    }
    return p;
}

fn print_problem(p: &Problem) {
    for i in 0 .. p.len() {
        print!("{} ", p.get(i).unwrap().value);
    }
    println!();
}

fn part1(filename: &str) -> isize {
    let mut p = load(filename);

    for order in 0 .. p.len() {
        //print_problem(&p);
        
        // Find the number to be moved
        let mut old_index: usize = usize::MAX;
        for i in 0 .. p.len() {
            if p.get(i).unwrap().order == order {
                old_index = i;
                break;
            }
        }
        assert!(old_index < p.len());
        // Remove
        let number: Number = *p.get(old_index).unwrap();
        p.remove(old_index);

        // What's the new position?
        let mut pos: isize = ((number.value + (old_index as isize)) 
                            % (p.len() as isize)) as isize;
        if pos <= 0 {
            pos += p.len() as isize;
        }
        let new_index = pos as usize;
        assert!(new_index <= p.len());

        // Insert in new position
        p.insert(new_index as usize, number);
    }
    //print_problem(&p);

    // Find zero
    let mut zero_index: usize = usize::MAX;
    for i in 0 .. p.len() {
        if p.get(i).unwrap().value == 0 {
            zero_index = i;
            break;
        }
    }
    assert!(zero_index < p.len());
    let a = p.get((zero_index + 1000) % p.len()).unwrap().value;
    let b = p.get((zero_index + 2000) % p.len()).unwrap().value;
    let c = p.get((zero_index + 3000) % p.len()).unwrap().value;
    println!("1000th is {}, 2000th is {}, 3000th is {}", a, b, c);
    return a + b + c;
}

#[test]
fn test_part1() {
    assert_eq!(part1(&"test"), 3);
}

fn main() {
    println!("{}", part1(&"input"));
}

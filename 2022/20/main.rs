
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

fn mix(p: &mut Problem) {
    // It can be tricky to avoid off-by-one errors in something like
    // this. The best way to get the code right is to compare to the
    // expected results given in the problem.
    // The operations used here are all O(N) - not very efficient - but
    // because of the relative difficulty of getting the code right in
    // the first place, I wasn't keen to try anything more complex. The
    // list size is only 5000 items anyway.
    for order in 0 .. p.len() {
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
}

fn get_coords(p: &Problem) -> isize {
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
    return a + b + c;
}

fn part1(filename: &str) -> isize {
    let mut p = load(filename);
    mix(&mut p);
    return get_coords(&p);
}

fn part2(filename: &str) -> isize {
    let mut p = load(filename);
    for i in 0 .. p.len() {
        p.get_mut(i).unwrap().value *= 811589153;
    }
    for _ in 0 .. 10 {
        mix(&mut p);
    }
    return get_coords(&p);
}

#[test]
fn test_part1() {
    assert_eq!(part1(&"test"), 3);
}

#[test]
fn test_part2() {
    assert_eq!(part2(&"test"), 1623178306);
}

fn main() {
    println!("{}", part1(&"input"));
    println!("{}", part2(&"input"));
}

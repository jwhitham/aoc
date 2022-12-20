
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::VecDeque;

#[derive(Copy, Clone)]
struct Number {
    value: isize,
    order: usize,
}

type Problem = VecDeque<Number>;

fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p: Problem = Problem::new();
    let mut order: usize = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            p.push_back(Number {
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
    // example intermediate results given in the problem.
    //
    // Use of rotation (with VecDeque) makes the code a lot simpler
    // but prevents easy comparison to the examples. It's also more
    // efficient.. however, there is still an O(N) search for the
    // next number to be processed. The list size is only 5000 items
    // though.
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
        p.rotate_left(old_index);
        let number: Number = p.pop_front().unwrap();
        assert_eq!(number.order, order);

        // What's the new position?
        let pos: isize = number.value % (p.len() as isize);

        // Insert in new position
        if pos < 0 {
            p.rotate_right((-pos) as usize);
        } else {
            p.rotate_left(pos as usize);
        }
        p.push_front(number);
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

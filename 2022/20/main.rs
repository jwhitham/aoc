
use std::fs::File;
use std::io::{self, BufRead};

extern crate tree_list;
use tree_list::TreeList;

struct Problem {
    orders: TreeList,
    order_to_value: Vec<isize>,
}

fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p = Problem {
        orders: TreeList::new(),
        order_to_value: Vec::new(),
    };
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let value: isize = line_string.parse().expect("n");
            let order: usize = p.order_to_value.len();
            p.orders.insert(order);
            p.order_to_value.push(value);
        }
    }
    return p;
}

fn mix(p: &mut Problem) {
    for order in 0 .. p.orders.len() {
        // Find the index of the number to be moved
        let old_index: usize = p.find(order).unwrap();
        assert!(old_index < p.len());

        // Remove
        p.orders.remove(old_index);

        // Value of number
        let value: isize = p.order_to_value(order).unwrap();

        // What's the new position?
        let pos: isize = value % (p.len() as isize);

        // Insert in new position
        if pos < 0 {
            pos += p.len() as isize;
        }
        p.insert(pos as usize, order);
    }
}

fn get_coords(p: &Problem) -> isize {
    // Find zero
    let mut zero_index: usize = usize::MAX;
    for order in 0 .. p.orders.len() {
        let value: isize = p.order_to_value(order).unwrap();
        if value == 0 {
            zero_index = p.orders.find(order).unwrap();
            break;
        }
    }
    assert!(zero_index < p.orders.len());
    let a = p.orders.get((zero_index + 1000) % p.orders.len()).unwrap().value;
    let b = p.orders.get((zero_index + 2000) % p.orders.len()).unwrap().value;
    let c = p.orders.get((zero_index + 3000) % p.orders.len()).unwrap().value;
    return a + b + c;
}

fn part1(filename: &str) -> isize {
    let mut p = load(filename);
    mix(&mut p);
    return get_coords(&p);
}

fn part2(filename: &str) -> isize {
    let mut p = load(filename);
    for order in 0 .. p.orders.len() {
        *p.order_to_value.get_mut(order) *= 811589153;
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

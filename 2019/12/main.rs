
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;


const NUM_DIMENSIONS: usize = 3;
type Word = i32;

#[derive(Copy, Clone)]
struct Dimension {
    position: Word,
    velocity: Word,
}

type Planet = [Dimension; 3];
type System = Vec<Planet>;

fn load_values(filename: &str) -> System {
    let file = File::open(filename).unwrap();
    let mut system: System = Vec::new();

    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let cleaned = line_string.replace("=", " ")
                                     .replace(",", " ")
                                     .replace(">", " ");
            let fields = Vec::from_iter(cleaned.split_ascii_whitespace());
            assert!(fields.len() >= 6);
            let p = [
                Dimension {
                    position: fields.get(1).unwrap().parse().expect("x"),
                    velocity: 0,
                },
                Dimension {
                    position: fields.get(3).unwrap().parse().expect("y"),
                    velocity: 0,
                },
                Dimension {
                    position: fields.get(5).unwrap().parse().expect("z"),
                    velocity: 0,
                },
            ];
            system.push(p);
        }
    }
    return system;
}

fn part1(filename: &str, num_steps: usize) -> Word {
    let mut system = load_values(filename);

    // For each time step
    for _ in 0 .. num_steps {
        // For each dimension
        for d in 0 .. NUM_DIMENSIONS {
            // Gravity
            for p1 in 0 .. system.len() {
                let pos1 = system.get(p1).unwrap()[d].position;
                for p2 in 0 .. system.len() {
                    let pos2 = system.get(p2).unwrap()[d].position;
                    if pos1 < pos2 {
                        system.get_mut(p1).unwrap()[d].velocity += 1;
                    } else if pos1 > pos2 {
                        system.get_mut(p1).unwrap()[d].velocity -= 1;
                    }
                }
            }
            // Position
            for p1 in 0 .. system.len() {
                system.get_mut(p1).unwrap()[d].position +=
                    system.get(p1).unwrap()[d].velocity;
            }
        }
    }
    // total energy
    let mut total: Word = 0;
    for p1 in 0 .. system.len() {
        let mut energy1: Word = 0;
        let mut energy2: Word = 0;
        for d in 0 .. NUM_DIMENSIONS {
            energy1 += Word::abs(system.get(p1).unwrap()[d].position);
            energy2 += Word::abs(system.get(p1).unwrap()[d].velocity);
        }
        total += energy1 * energy2;
    }
    return total;
}

#[test]
fn test_part1() {
    assert_eq!(part1("test", 10), 179);
    assert_eq!(part1("test2", 100), 1940);
}

fn get_period(initial: &System, d: usize) -> usize {
    // copy of initial state
    let mut system: System = initial.clone();

    // For each time step
    let mut num_steps: usize = 0;
    let mut accept: bool = false;
    while !accept {
        // Gravity
        for p1 in 0 .. system.len() {
            let pos1 = system.get(p1).unwrap()[d].position;
            for p2 in 0 .. system.len() {
                let pos2 = system.get(p2).unwrap()[d].position;
                if pos1 < pos2 {
                    system.get_mut(p1).unwrap()[d].velocity += 1;
                } else if pos1 > pos2 {
                    system.get_mut(p1).unwrap()[d].velocity -= 1;
                }
            }
        }
        // Position
        for p1 in 0 .. system.len() {
            system.get_mut(p1).unwrap()[d].position +=
                system.get(p1).unwrap()[d].velocity;
        }
        // Returned to initial state?
        accept = true;
        for p1 in 0 .. system.len() {
            if (system.get_mut(p1).unwrap()[d].position !=
                    initial.get(p1).unwrap()[d].position)
            || (system.get_mut(p1).unwrap()[d].velocity !=
                    initial.get(p1).unwrap()[d].velocity) {
                accept = false;
                break;
            }
        }
        num_steps += 1;
    }
    return num_steps;
}

fn greatest_common_divisor(a: usize, b: usize) -> usize {
    let mut copy_a = a;
    let mut copy_b = b;
    loop {
        copy_a %= copy_b;
        if copy_a == 0 {
            return copy_b;
        }
        copy_b %= copy_a;
        if copy_b == 0 {
            return copy_a;
        }
    }
}

fn least_common_multiple(a: usize, b: usize) -> usize {
    return (a * b) / greatest_common_divisor(a, b);
}

fn part2(filename: &str) -> usize {
    let system = load_values(filename);

    let px = get_period(&system, 0);
    let py = get_period(&system, 1);
    let pz = get_period(&system, 2);
    return least_common_multiple(px, least_common_multiple(py, pz));
}

#[test]
fn test_part2() {
    assert_eq!(part2("test"), 2772);
    assert_eq!(part2("test2"), 4686774924);
}

fn main() {
    println!("{}", part1("input", 1000));
    println!("{}", part2("input"));
}



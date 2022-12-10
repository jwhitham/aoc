
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;


const NUM_DIMENSIONS: usize = 3;
const NUM_PLANETS: usize = 4;

type Word = i16;
type Time = u64;

#[derive(Copy, Clone)]
struct Dimension {
    position: Word,
    velocity: Word,
}

type Planet = [Dimension; NUM_DIMENSIONS];
type System = [Planet; NUM_PLANETS];

fn load_values(filename: &str) -> System {
    let file = File::open(filename).unwrap();
    let mut system: System = [[Dimension {
        position: 0,
        velocity: 0,
    }; NUM_DIMENSIONS]; NUM_PLANETS];
    let mut p1: usize = 0;

    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let cleaned = line_string.replace("=", " ")
                                     .replace(",", " ")
                                     .replace(">", " ");
            let fields = Vec::from_iter(cleaned.split_ascii_whitespace());
            assert!(fields.len() >= 6);
            assert!(p1 < NUM_PLANETS);
            for d in 0 .. NUM_DIMENSIONS {
                system[p1][d].position =
                    fields.get((d * 2) + 1).unwrap().parse().expect("x");
            }
            p1 += 1;
        }
    }
    return system;
}

fn simulate(system: &mut System, d: usize) {
    // Gravity
    for p1 in 0 .. NUM_PLANETS {
        let pos1 = system[p1][d].position;
        for p2 in 0 .. NUM_PLANETS {
            let pos2 = system[p2][d].position;
            if pos1 < pos2 {
                system[p1][d].velocity += 1;
            } else if pos1 > pos2 {
                system[p1][d].velocity -= 1;
            }
        }
    }
    // Position
    for p1 in 0 .. NUM_PLANETS {
        system[p1][d].position +=
            system[p1][d].velocity;
    }
}

fn part1(filename: &str, num_steps: Time) -> Word {
    let mut system = load_values(filename);

    // For each time step
    for _ in 0 .. num_steps {
        // For each dimension
        for d in 0 .. NUM_DIMENSIONS {
            simulate(&mut system, d);
        }
    }
    // total energy
    let mut total: Word = 0;
    for p1 in 0 .. NUM_PLANETS {
        let mut energy1: Word = 0;
        let mut energy2: Word = 0;
        for d in 0 .. NUM_DIMENSIONS {
            energy1 += Word::abs(system[p1][d].position);
            energy2 += Word::abs(system[p1][d].velocity);
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

fn get_period(initial: &System, d: usize) -> Time {
    // copy of initial state
    let mut system: System = initial.clone();

    // For each time step
    let mut num_steps: Time = 0;
    let mut accept: bool = false;
    while !accept {
        // Simulate this dimension only
        simulate(&mut system, d);

        // Returned to initial state?
        accept = true;
        for p1 in 0 .. NUM_PLANETS {
            if (system[p1][d].position != initial[p1][d].position)
            || (system[p1][d].velocity != initial[p1][d].velocity) {
                accept = false;
                break;
            }
        }
        num_steps += 1;
    }
    return num_steps;
}

fn greatest_common_divisor(a: Time, b: Time) -> Time {
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

fn least_common_multiple(a: Time, b: Time) -> Time {
    return (a * b) / greatest_common_divisor(a, b);
}

fn part2(filename: &str) -> Time {
    let system = load_values(filename);

    // Calculate period for each dimension individually
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



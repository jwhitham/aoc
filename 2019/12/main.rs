
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;


const NUM_DIMENSIONS: usize = 3;
type Word = i32;

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
        /*
        println!("After {} steps", step);
        for p1 in 0 .. system.len() {
            print!("pos=<");
            for d in 0 .. NUM_DIMENSIONS {
                print!(" {} ", system.get(p1).unwrap()[d].position);
            }
            print!("> vel=<");
            for d in 0 .. NUM_DIMENSIONS {
                print!(" {} ", system.get(p1).unwrap()[d].velocity);
            }
            println!(">");
        }
        println!();
        */

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

fn main() {
    println!("{}", part1("input", 1000));
}




use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;
use std::iter::FromIterator;

type Word = i8;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Location {
    x: Word,
    y: Word,
    z: Word,
}

type Problem = HashSet<Location>;
type ExposedFaceCount = u32;

fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p: Problem = Problem::new();
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let cleaned = line_string.replace(",", " ");
            let fields = Vec::from_iter(cleaned.split_ascii_whitespace());
            assert_eq!(fields.len(), 3);
            p.insert(Location {
                x: fields.get(0).unwrap().parse().expect("x"),
                y: fields.get(1).unwrap().parse().expect("y"),
                z: fields.get(2).unwrap().parse().expect("z"),
            });
        }
    }
    return p;
}

fn part1(problem: &Problem) -> ExposedFaceCount {
    let mut efc: ExposedFaceCount = 0;

    for cube0 in problem {
        let mut test_face = |dx: Word, dy: Word, dz: Word| {
            if !problem.contains(&Location {
                x: cube0.x + dx, 
                y: cube0.y + dy, 
                z: cube0.z + dz, 
            }) {
                efc += 1;
            }
        };
        test_face(-1, 0, 0);
        test_face(1, 0, 0);
        test_face(0, -1, 0);
        test_face(0, 1, 0);
        test_face(0, 0, -1);
        test_face(0, 0, 1);
    }
    return efc;
}

#[test]
fn test_part1() {
    assert_eq!(part1(&load("test")), 64);
}

fn main() {
    println!("{}", part1(&load("input")));
}



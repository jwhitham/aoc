
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;
use std::iter::FromIterator;

type Word = i8;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Location {
    x: Word,
    y: Word,
    z: Word,
}

#[derive(Eq, PartialEq, Copy, Clone)]
enum Item {
    Open,
    Lava,
    Unknown,
}

type Problem = HashMap<Location, Item>;
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
            }, Item::Lava);
        }
    }
    return p;
}

fn part1(problem: &Problem) -> ExposedFaceCount {
    let mut efc: ExposedFaceCount = 0;

    for cube0 in problem.keys() {
        let mut test_face = |dx: Word, dy: Word, dz: Word| {
            if !problem.contains_key(&Location {
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

fn flood_fill(cube0: &Location, min_bbox: &Location, max_bbox: &Location,
              problem: &mut Problem, dx: Word, dy: Word, dz: Word) {
    let mut cube1 = *cube0;

    // Step in the given direction
    cube1.x += dx;
    cube1.y += dy;
    cube1.z += dz;
    // Anything known at this location?
    if problem.contains_key(&cube1) {
        return;
    }
    // Are we still inside the bbox?
    if (cube1.x < min_bbox.x) || (cube1.x > max_bbox.x)
    || (cube1.y < min_bbox.y) || (cube1.y > max_bbox.y)
    || (cube1.z < min_bbox.z) || (cube1.z > max_bbox.z) {
        return;
    }
    // This place is exposed
    problem.insert(cube1, Item::Open);
    flood_fill(&cube1, min_bbox, max_bbox, problem, -1,  0,  0);
    flood_fill(&cube1, min_bbox, max_bbox, problem,  1,  0,  0);
    flood_fill(&cube1, min_bbox, max_bbox, problem,  0, -1,  0);
    flood_fill(&cube1, min_bbox, max_bbox, problem,  0,  1,  0);
    flood_fill(&cube1, min_bbox, max_bbox, problem,  0,  0, -1);
    flood_fill(&cube1, min_bbox, max_bbox, problem,  0,  0,  1);
}

fn part2(problem: &Problem) -> ExposedFaceCount {

    // Find the bounding box for the problem - anything outside of this
    // is always exposed. The bounding box is larger than the actual problem
    // by one cube so that all exposed areas can be marked as exposed.
    let mut min_bbox = Location { x: Word::MAX, y: Word::MAX, z: Word::MAX };
    let mut max_bbox = Location { x: Word::MIN, y: Word::MIN, z: Word::MIN };
    for cube0 in problem.keys() {
        min_bbox.x = Word::min(cube0.x - 1, min_bbox.x);
        min_bbox.y = Word::min(cube0.y - 1, min_bbox.y);
        min_bbox.z = Word::min(cube0.z - 1, min_bbox.z);
        max_bbox.x = Word::max(cube0.x + 1, max_bbox.x);
        max_bbox.y = Word::max(cube0.y + 1, max_bbox.y);
        max_bbox.z = Word::max(cube0.z + 1, max_bbox.z);
    }

    // Fill all exposed cells with the invisible Item::Open.
    let mut flooded = problem.clone();
    flood_fill(&min_bbox, &min_bbox, &max_bbox, &mut flooded, 0, 0, 0);

    // What's exposed? An Item::Lava face is connected to an Item::Open face.
    let mut efc: ExposedFaceCount = 0;
    for cube0 in problem.keys() {
        let mut test_face = |dx: Word, dy: Word, dz: Word| {
            if *flooded.get(&Location {
                x: cube0.x + dx, 
                y: cube0.y + dy, 
                z: cube0.z + dz, 
            }).unwrap_or(&Item::Unknown) == Item::Open {
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
fn test_part2() {
    assert_eq!(part2(&load("test")), 58);
}

fn main() {
    println!("{}", part1(&load("input")));
    println!("{}", part2(&load("input")));
}



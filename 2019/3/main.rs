
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;


#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}

fn distance(point: &Point) -> i32 {
    return point.x.abs() + point.y.abs();
}

fn trace_line(steps: &str) -> HashSet<Point> {

    let mut location = Point { x: 0, y: 0 };
    let mut line: HashSet<Point> = HashSet::new();

    for step in steps.split(",") {
        let direction: u8 = step[0..1].as_bytes()[0];
        let mut count: i32 = step[1..].parse().expect("count");

        while count > 0 {
            match direction {
                b'R' => location.x += 1,
                b'L' => location.x -= 1,
                b'U' => location.y -= 1,
                b'D' => location.y += 1,
                _ => panic!(),
            }
            count -= 1;
            line.insert(location);
        }
    }
    return line;
}

fn main() {
    // read input
    let file = File::open("input").unwrap();
    let mut lines = io::BufReader::new(file).lines();
    let line1 = lines.next().expect("line 1").unwrap();
    let line2 = lines.next().expect("line 2").unwrap();
    let line1_set = trace_line(line1.trim());
    let line2_set = trace_line(line2.trim());

    // find closest point
    let mut best_distance = i32::MAX;
    for point in line1_set.intersection(&line2_set) {
        let d = distance(point);
        best_distance = i32::min(d, best_distance);
    }
    println!("{}", best_distance);
}
   

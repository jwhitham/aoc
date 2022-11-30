
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;


#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}

fn distance(point: &Point) -> i32 {
    return point.x.abs() + point.y.abs();
}

fn trace_line(steps: &str) -> HashMap<Point, u32> {

    let mut location = Point { x: 0, y: 0 };
    let mut line: HashMap<Point, u32> = HashMap::new();
    let mut total_count: u32 = 0;

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
            total_count += 1;
            if !line.contains_key(&location) {
                line.insert(location, total_count);
            }
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
    let line1_map = trace_line(line1.trim());
    let line2_map = trace_line(line2.trim());

    // part 1: find closest point (Manhattan distance from 0,0)
    let mut best_distance = i32::MAX;
    for point in line1_map.keys() {
        if line2_map.contains_key(&point) {
            let d = distance(&point);
            best_distance = i32::min(d, best_distance);
        }
    }
    println!("{}", best_distance);

    // part 2: find closest point (propagation delay)
    let mut best_delay = u32::MAX;
    for point in line1_map.keys() {
        if let Some (d2) = line2_map.get(&point) {
            let d1 = line1_map.get(&point).unwrap();
            best_delay = u32::min(d1 + d2, best_delay);
        }
    }
    println!("{}", best_delay);
}
   

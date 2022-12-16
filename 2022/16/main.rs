
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashMap;



type FlowRate = u32;
type ValveId = String;

struct Valve {
    id: ValveId,
    flow_rate: FlowRate,
    tunnel_to: Vec<ValveId>,
}

type Problem = HashMap<ValveId, Valve>;

// Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
// 0     1  2   3    4    5  6       7    8  9      10...

fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p = Problem::new();
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let cleaned = line_string.replace("=", " ")
                                     .replace(",", " ")
                                     .replace(";", " ");
            let fields = Vec::from_iter(cleaned.split_ascii_whitespace());
            assert_eq!(*fields.get(0).unwrap(), "Valve");
            assert_eq!(*fields.get(2).unwrap(), "has");
            assert_eq!(*fields.get(8).unwrap(), "to");

            let id = fields.get(1).unwrap().to_string();
            let mut valve = Valve {
                id: id.clone(),
                flow_rate: fields.get(5).unwrap().parse().expect("fr"),
                tunnel_to: Vec::new(),
            };
            for i in 10 .. fields.len() {
                valve.tunnel_to.push(fields.get(i).unwrap().to_string());
            }
            p.insert(id, valve);
        }
    }
    return p;
}

fn part1(problem: &Problem) -> FlowRate {
    return 0;
}

#[test]
fn test_part1() {
    assert_eq!(part1(&load("test")), 1651);
}

fn main() {
    println!("{}", part1(&load("input")));
}



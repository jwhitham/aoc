
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::BinaryHeap;
use std::cmp::Ordering;



type FlowRate = u32;
type ValveId = String;
type Time = u8;

#[derive(Clone)]
struct Path {
    id: ValveId,
    time: Time,
}

impl Eq for Path {}

impl PartialEq for Path {
    fn eq(&self, other: &Self) -> bool {
        return self.cmp(other) == Ordering::Equal;
    }
}

impl PartialOrd for Path {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        return Some(self.cmp(other));
    }
}

impl Ord for Path {
    fn cmp(&self, other: &Self) -> Ordering {
        // Need a min-heap so the order is reversed
        if self.time > other.time {
            return Ordering::Less;
        } else if self.time < other.time {
            return Ordering::Greater;
        } else {
            return Ordering::Equal;
        }
    }
}

type PathTo = HashMap<ValveId, Path>;
type PathFromTo = HashMap<ValveId, PathTo>;
type Visited = HashSet<ValveId>;
type ValveMap = HashMap<ValveId, Valve>;

struct Valve {
    flow_rate: FlowRate,
    tunnel_to: Vec<ValveId>,
}

// Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
// 0     1  2   3    4    5  6       7    8  9      10...

fn load(filename: &str) -> ValveMap {
    let file = File::open(filename).unwrap();
    let mut v = ValveMap::new();
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
                flow_rate: fields.get(5).unwrap().parse().expect("fr"),
                tunnel_to: Vec::new(),
            };
            for i in 10 .. fields.len() {
                valve.tunnel_to.push(fields.get(i).unwrap().to_string());
            }
            v.insert(id, valve);
        }
    }
    return v;
}

fn compute_shortest_paths(valves: &ValveMap, valve1_id: &String) -> PathTo {
    // Initialise best paths for this valve
    let mut best_path_to: PathTo = HashMap::new();
    for valve2_id in valves.keys() {
        best_path_to.insert(valve2_id.clone(), Path {
            id: valve2_id.clone(),
            time: Time::MAX,
        });
    }

    // Solve shortest-path problem starting at valve 1
    let mut todo: BinaryHeap<Path> = BinaryHeap::new();
    todo.push(Path {
        id: valve1_id.clone(),
        time: 0,
    });

    while !todo.is_empty() {
        // Process shortest-path problem at intermediate valve 2
        let valve2_path: Path = todo.pop().unwrap();

        // Shortest path found to this valve
        best_path_to.get_mut(&valve2_path.id).unwrap().time = valve2_path.time;

        // Process all tunnels from here
        for valve3_id in valves.get(&valve2_path.id).unwrap().tunnel_to.iter() {
            if best_path_to.get(valve3_id).unwrap().time == Time::MAX {
                // Intermediate valve 3 not processed yet - possible path found
                todo.push(Path {
                    id: valve3_id.clone(),
                    time: valve2_path.time + 1,
                });
            }
        }
    }

    // Keep useful path information
    let mut useful_path_to: PathTo = HashMap::new();
    for (valve2_id, path) in best_path_to {
        if (valves.get(&valve2_id).unwrap().flow_rate != 0) && (valve2_id != *valve1_id) {
            useful_path_to.insert(valve2_id.clone(), path);
        }
    }
    return useful_path_to;
}

fn compute_best_sequence(valves: &ValveMap,
                         path_from_to: &PathFromTo,
                         visited: &mut Visited,
                         valve1_id: &String, time_left: Time) -> FlowRate {
    assert!(!visited.contains(valve1_id));
    visited.insert(valve1_id.clone());

    // What do we get by turning off the valve here?
    let self_flow_rate: FlowRate = valves.get(valve1_id).unwrap().flow_rate * (time_left as FlowRate);

    // Where do we go next?
    let mut sub_flow_rate = 0;
    for (valve2_id, path) in path_from_to.get(valve1_id).unwrap().iter() {
        if !visited.contains(valve2_id) {
            let sub_time = path.time + 1;
            if sub_time <= time_left {
                sub_flow_rate = FlowRate::max(sub_flow_rate,
                                   compute_best_sequence(valves, path_from_to,
                                                         visited, valve2_id, time_left - sub_time));
            }
        }
    }
    visited.remove(valve1_id);
    return sub_flow_rate + self_flow_rate;
}

fn part1(valves: &ValveMap) -> FlowRate {
    let mut path_from_to = PathFromTo::new();
    let mut visited = Visited::new();

    // Compute shortest paths betwen valves
    for valve1_id in valves.keys() {
        path_from_to.insert(valve1_id.clone(), compute_shortest_paths(&valves, valve1_id));
    }

    // Solve the problem starting at AA
    return compute_best_sequence(&valves, &path_from_to, &mut visited, &"AA".to_string(), 30);
}

#[test]
fn test_part1() {
    assert_eq!(part1(&load("test")), 1651);
}

fn main() {
    println!("{}", part1(&load("input")));
}



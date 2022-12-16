
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::BinaryHeap;
use std::cmp::Ordering;



type FlowRate = u32;
type ValveId = u16;
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

type PathTo = Vec<Path>;
type PathFromTo = HashMap<ValveId, PathTo>;
type Visited = HashSet<ValveId>;
type ValveMap = HashMap<ValveId, Valve>;

struct Valve {
    flow_rate: FlowRate,
    tunnel_to: Vec<ValveId>,
}

struct ProblemState {
    visited: Visited,
    upper_bound: FlowRate,
    best_result: FlowRate,
    lost_flow_per_minute: FlowRate,
    total_flow: FlowRate,
    time: Time,
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

            let id = get_valve_id(fields.get(1).unwrap());
            let mut valve = Valve {
                flow_rate: fields.get(5).unwrap().parse().expect("fr"),
                tunnel_to: Vec::new(),
            };
            for i in 10 .. fields.len() {
                valve.tunnel_to.push(get_valve_id(fields.get(i).unwrap()));
            }
            v.insert(id, valve);
        }
    }
    return v;
}

fn get_valve_id(name: &str) -> ValveId {
    let mut id: ValveId = 0;
    for byte in name.bytes() {
        id *= 256;
        id |= byte as ValveId;
    }
    return id;
}

fn compute_shortest_paths(valves: &ValveMap, valve1_id: ValveId) -> PathTo {
    // Initialise best paths for this valve
    let mut best_path_to: HashMap<ValveId, Path> = HashMap::new();
    for valve2_id in valves.keys() {
        best_path_to.insert(*valve2_id, Path {
            id: *valve2_id,
            time: Time::MAX,
        });
    }

    // Solve shortest-path problem starting at valve 1
    let mut todo: BinaryHeap<Path> = BinaryHeap::new();
    todo.push(Path {
        id: valve1_id,
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
                    id: *valve3_id,
                    time: valve2_path.time + 1,
                });
            }
        }
    }

    // Keep useful path information
    let mut useful_path_to: PathTo = PathTo::new();
    for (valve2_id, path) in best_path_to {
        if (valves.get(&valve2_id).unwrap().flow_rate != 0) && (valve2_id != valve1_id) {
            useful_path_to.push(path);
        }
    }
    return useful_path_to;
}

const PART1_TIME: Time = 30;

fn compute_best_sequence1(valves: &ValveMap,
                          path_from_to: &PathFromTo,
                          part1: &mut ProblemState,
                          valve1_id: ValveId,
                          travel_time: Time) {
    // Can we make it in time?
    if (part1.time + travel_time) >= PART1_TIME {
        return;
    }

    // Update the upper bound based on the lost flow per minute
    part1.upper_bound -= part1.lost_flow_per_minute * (travel_time as FlowRate);

    // Only visit this valve if the solution could be an improvement
    if part1.upper_bound > part1.total_flow {
        // Visit this valve - what do we get by turning off the valve here?
        part1.visited.insert(valve1_id);
        part1.time += travel_time;
        let time_left: Time = PART1_TIME - part1.time;
        let flow_rate: FlowRate = valves.get(&valve1_id).unwrap().flow_rate;
        part1.total_flow += flow_rate * (time_left as FlowRate);
        part1.lost_flow_per_minute -= flow_rate;

        // Where do we go next?
        for path in path_from_to.get(&valve1_id).unwrap().iter() {
            if !part1.visited.contains(&path.id) {
                let travel_time = path.time + 1;
                compute_best_sequence1(valves, path_from_to, part1, path.id, travel_time);
            }
        }

        // Record new result if any
        if part1.total_flow > part1.best_result {
            part1.best_result = part1.total_flow;
        }

        // Restore state
        part1.lost_flow_per_minute += flow_rate;
        part1.total_flow -= flow_rate * (time_left as FlowRate);
        part1.time -= travel_time;
        part1.visited.remove(&valve1_id);
    }

    // Restore upper bound
    part1.upper_bound += part1.lost_flow_per_minute * (travel_time as FlowRate);
}

fn part1(valves: &ValveMap) -> FlowRate {
    let mut path_from_to = PathFromTo::new();
    let mut part1 = ProblemState {
        visited: Visited::new(),
        upper_bound: 0,
        best_result: 0,
        total_flow: 0,
        lost_flow_per_minute: 0,
        time: 0,
    };

    // Compute shortest paths betwen valves
    for valve1_id in valves.keys() {
        path_from_to.insert(*valve1_id, compute_shortest_paths(&valves, *valve1_id));
    }

    // Compute the best possible flow rate assuming all valves are turned on
    for valve1 in valves.values() {
        part1.lost_flow_per_minute += valve1.flow_rate;
    }
    part1.upper_bound = part1.lost_flow_per_minute * (PART1_TIME as FlowRate);

    // Solve the problem starting at AA
    compute_best_sequence1(&valves, &path_from_to, &mut part1, get_valve_id("AA"), 0);
    return part1.best_result;
}

const PART2_TIME: Time = 26;

fn compute_best_sequence2(valves: &ValveMap,
                         path_from_to: &PathFromTo,
                         visited: &mut Visited,
                         p1_valve1_id: ValveId,
                         p1_ready_at: Time,
                         p2_valve1_id: ValveId,
                         p2_ready_at: Time) -> FlowRate {


    // Use location and time for whoever moves first
    // This does not seem to be a good solution.
    // I think there must be a way to cut down the search space.
    let move_ready_at: Time;
    let move_valve1_id: ValveId;
    let next_ready_at: Time;
    let next_valve1_id: ValveId;
    if p1_ready_at <= p2_ready_at {
        move_ready_at = p1_ready_at;
        move_valve1_id = p1_valve1_id;
        next_ready_at = p2_ready_at;
        next_valve1_id = p2_valve1_id;
    } else {
        move_ready_at = p2_ready_at;
        move_valve1_id = p2_valve1_id;
        next_ready_at = p1_ready_at;
        next_valve1_id = p1_valve1_id;
    }
    assert!(move_ready_at < PART2_TIME);
    assert!(next_ready_at < PART2_TIME);

    let mut best_flow_rate = 0;
    for path in path_from_to.get(&move_valve1_id).unwrap().iter() {
        if !visited.contains(&path.id) {
            assert!(!visited.contains(&path.id));
            let sub_ready_at = path.time + 1 + move_ready_at;
            if sub_ready_at < PART2_TIME {
                visited.insert(path.id);

                let time_left: Time = PART2_TIME - sub_ready_at;
                let sub_flow_rate: FlowRate =
                    (valves.get(&path.id).unwrap().flow_rate * (time_left as FlowRate)) +
                    compute_best_sequence2(valves, path_from_to, visited,
                                           path.id, sub_ready_at,
                                           next_valve1_id, next_ready_at);
                assert!(visited.contains(&path.id));
                visited.remove(&path.id);

                best_flow_rate = FlowRate::max(best_flow_rate, sub_flow_rate);
            }
        }
    }

    return best_flow_rate;
}

fn part2(valves: &ValveMap) -> FlowRate {
    let mut path_from_to = PathFromTo::new();
    let mut visited = Visited::new();

    // Compute shortest paths betwen valves
    for valve1_id in valves.keys() {
        path_from_to.insert(*valve1_id, compute_shortest_paths(&valves, *valve1_id));
    }

    // Solve the problem starting at AA
    return compute_best_sequence2(&valves, &path_from_to, &mut visited,
                                  get_valve_id("AA"), 0,
                                  get_valve_id("AA"), 0);
}

#[test]
fn test_part1() {
    assert_eq!(part1(&load("test")), 1651);
    assert_eq!(part1(&load("input")), 2056);
}

#[test]
fn test_part2() {
    assert_eq!(part2(&load("test")), 1707);
}

fn main() {
    println!("{}", part1(&load("input")));
    //println!("{}", part2(&load("input")));
}



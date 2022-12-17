
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
            // The order doesn't matter, except so that we can have the same
            // path through the algorithm every time (not dependent on hashing)
            return self.id.cmp(&other.id);
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
    plan_to_visit: Visited,
    upper_bound: FlowRate,
    best_result: FlowRate,
    lost_flow_per_minute: FlowRate,
    total_flow: FlowRate,
    time: Time,
    total_time: Time,
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
        id <<= 8;
        id |= byte as ValveId;
    }
    return id;
}

fn get_start_valve_id() -> ValveId {
    return get_valve_id("AA");
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

    // It's best to process the shortest paths first
    useful_path_to.sort();
    useful_path_to.reverse();
    return useful_path_to;
}

fn compute_best_sequence(valves: &ValveMap,
                         path_from_to: &PathFromTo,
                         ps: &mut ProblemState,
                         valve1_id: ValveId,
                         travel1_time: Time,
                         valve2_id: ValveId,
                         travel2_time: Time) {

    let travel_time: Time;
    let other_time: Time;
    let valve_id: ValveId;
    let other_valve_id: ValveId;

    // Who arrives first, and where?
    if travel1_time <= travel2_time {
        travel_time = travel1_time;
        valve_id = valve1_id;
        other_time = travel2_time - travel1_time;
        other_valve_id = valve2_id;
    } else {
        travel_time = travel2_time;
        valve_id = valve2_id;
        other_time = travel1_time - travel2_time;
        other_valve_id = valve1_id;
    }

    // Can we make it in time?
    if (ps.time + travel_time) >= ps.total_time {
        return;
    }

    // Update the upper bound based on the lost flow per minute
    // This is the maximum achievable flow assuming all valves immediately open
    ps.upper_bound -= ps.lost_flow_per_minute * (travel_time as FlowRate);

    // Advance the simulated time
    ps.time += travel_time;

    // Visit this valve - what do we get by turning off the valve here?
    let time_left: Time = ps.total_time - ps.time;
    let flow_rate: FlowRate = valves.get(&valve_id).unwrap().flow_rate;
    ps.total_flow += flow_rate * (time_left as FlowRate);
    ps.lost_flow_per_minute -= flow_rate;

    // Where do we go next?
    for path in path_from_to.get(&valve_id).unwrap().iter() {
        if ps.upper_bound <= ps.best_result {
            // prune this part of the search space
            break;
        }

        let sub_travel_time = path.time + 1;
        if (ps.time + sub_travel_time < ps.total_time)
        && (path.id != other_valve_id)
        && !ps.plan_to_visit.contains(&path.id) {
            ps.plan_to_visit.insert(path.id);
            compute_best_sequence(valves, path_from_to, ps,
                                  path.id, sub_travel_time,
                                  other_valve_id, other_time);
            ps.plan_to_visit.remove(&path.id);
        }
    }

    // Process the other direction by itself (necessary as a final move)
    if (ps.upper_bound > ps.best_result)
    && ps.plan_to_visit.contains(&other_valve_id) {
        compute_best_sequence(valves, path_from_to, ps,
                              other_valve_id, other_time,
                              0, ps.total_time);
    }

    // Record new result if any
    if ps.total_flow > ps.best_result {
        ps.best_result = ps.total_flow;
    }

    // Restore state
    ps.lost_flow_per_minute += flow_rate;
    ps.total_flow -= flow_rate * (time_left as FlowRate);
    ps.time -= travel_time;
    ps.upper_bound += ps.lost_flow_per_minute * (travel_time as FlowRate);
}

fn make_problem_state(valves: &ValveMap, total_time: Time) -> (ProblemState, PathFromTo) {
    let mut path_from_to = PathFromTo::new();
    let mut ps = ProblemState {
        plan_to_visit: Visited::new(),
        upper_bound: 0,
        best_result: 0,
        total_flow: 0,
        lost_flow_per_minute: 0,
        time: 0,
        total_time: total_time,
    };

    // Compute shortest paths betwen valves
    for valve_id in valves.keys() {
        path_from_to.insert(*valve_id, compute_shortest_paths(&valves, *valve_id));
    }

    // How much possible flow is lost every minute at the beginning of the puzzle?
    for valve in valves.values() {
        ps.lost_flow_per_minute += valve.flow_rate;
    }

    // Compute the best possible flow rate assuming all valves
    // are turned on immediately
    for valve in valves.values() {
        ps.upper_bound += valve.flow_rate * (total_time as FlowRate);
    }
    return (ps, path_from_to);
}

fn part1(valves: &ValveMap) -> FlowRate {
    let total_time: Time = 30;
    let (mut ps, path_from_to) = make_problem_state(valves, total_time);
    compute_best_sequence(&valves, &path_from_to, &mut ps,
                          get_start_valve_id(), 0,
                          0, total_time);
    return ps.best_result;
}

fn part2(valves: &ValveMap) -> FlowRate {
    let total_time: Time = 26;
    let (mut ps, path_from_to) = make_problem_state(valves, total_time);
    compute_best_sequence(&valves, &path_from_to, &mut ps,
                          get_start_valve_id(), 0,
                          get_start_valve_id(), 0);
    return ps.best_result;
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
    println!("{}", part2(&load("input")));
}



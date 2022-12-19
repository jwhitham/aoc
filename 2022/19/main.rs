
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;
use std::iter::FromIterator;

#[derive(Copy, Clone)]
struct Costs {
    ore_robot_ore_cost: u8,
    clay_robot_ore_cost: u8,
    obsidian_robot_ore_cost: u8,
    obsidian_robot_clay_cost: u8,
    geode_robot_ore_cost: u8,
    geode_robot_obsidian_cost: u8,
}

#[derive(Copy, Clone, Hash, Eq, PartialEq)]
struct State {
    ore: u8,
    clay: u8,
    obsidian: u8,
    geodes: u8,
    ore_robots: u8,
    clay_robots: u8,
    obsidian_robots: u8,
    geode_robots: u8,
    time_left: u8,
}

fn advance_state(state: &mut State) {
    state.time_left -= 1;
    state.ore += state.ore_robots;
    state.clay += state.clay_robots;
    state.obsidian += state.obsidian_robots;
    state.geodes += state.geode_robots;
}

fn evaluate(line_string: &str) -> u8 {
    let fields = Vec::from_iter(line_string.split_ascii_whitespace());
    assert_eq!(*fields.get(5).unwrap(), "costs");
    assert_eq!(*fields.get(31).unwrap(), "obsidian.");

    let costs = Costs {
        ore_robot_ore_cost: fields.get(6).unwrap().parse().expect("ore"),
        clay_robot_ore_cost: fields.get(12).unwrap().parse().expect("clay"),
        obsidian_robot_ore_cost: fields.get(18).unwrap().parse().expect("ore"),
        obsidian_robot_clay_cost: fields.get(21).unwrap().parse().expect("clay"),
        geode_robot_ore_cost: fields.get(27).unwrap().parse().expect("ore"),
        geode_robot_obsidian_cost: fields.get(30).unwrap().parse().expect("obsidian"),
    };

    let mut states: Vec<State> = Vec::new();
    let mut seen: HashSet<State> = HashSet::new();
    let mut best_geodes: u8 = 0;
    let total_time = 24;

    states.push(State {
        ore: 0,
        clay: 0,
        obsidian: 0,
        geodes: 0,
        ore_robots: 1,
        clay_robots: 0,
        obsidian_robots: 0,
        geode_robots: 0,
        time_left: total_time,
    });

    while let Some(cur_state) = states.pop() {
        if cur_state.time_left == 0 {
            best_geodes = u8::max(best_geodes, cur_state.geodes);
            continue;
        }
        if seen.contains(&cur_state) {
            continue;
        }
        if costs.ore_robot_ore_cost <= cur_state.ore {
            // build an ore robot
            let mut next_state: State = cur_state;
            advance_state(&mut next_state);
            next_state.ore -= costs.ore_robot_ore_cost;
            next_state.ore_robots += 1;
            states.push(next_state);
        }
        if costs.clay_robot_ore_cost <= cur_state.ore {
            // build a clay robot
            let mut next_state: State = cur_state;
            advance_state(&mut next_state);
            next_state.ore -= costs.clay_robot_ore_cost;
            next_state.clay_robots += 1;
            states.push(next_state);
        }
        if (costs.obsidian_robot_ore_cost <= cur_state.ore)
        && (costs.obsidian_robot_clay_cost <= cur_state.clay) {
            // build an obsidian robot
            let mut next_state: State = cur_state;
            advance_state(&mut next_state);
            next_state.ore -= costs.obsidian_robot_ore_cost;
            next_state.clay -= costs.obsidian_robot_clay_cost;
            next_state.obsidian_robots += 1;
            states.push(next_state);
        }
        if (costs.geode_robot_ore_cost <= cur_state.ore)
        && (costs.geode_robot_obsidian_cost <= cur_state.obsidian) {
            // build a geode robot
            let mut next_state: State = cur_state;
            advance_state(&mut next_state);
            next_state.ore -= costs.geode_robot_ore_cost;
            next_state.obsidian -= costs.geode_robot_obsidian_cost;
            next_state.geode_robots += 1;
            states.push(next_state);
        }
        // Or do nothing...
        {
            let mut next_state: State = cur_state;
            advance_state(&mut next_state);
            states.push(next_state);
        }
        seen.insert(cur_state);
    }
    return best_geodes;
}

#[test]
fn test_part1a() {
    assert_eq!(evaluate(&"Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian."), 9);
}

#[test]
fn test_part1b() {
    assert_eq!(evaluate(&"Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian."), 12);
}

fn part1(filename: &str) -> u32 {
    let file = File::open(filename).unwrap();
    let mut id: u32 = 0;
    let mut total: u32 = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            id += 1;
            let geodes = evaluate(line_string.as_str()) as u32;
            total += id * geodes;
        }
    }
    return total;
}

fn main() {
    println!("{}", part1(&"input"));
}

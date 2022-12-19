
use std::fs::File;
use std::io::{self, BufRead};
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

fn advance_state(state: &mut State, delta: u8) {
    state.time_left -= delta;
    state.ore += state.ore_robots * delta;
    state.clay += state.clay_robots * delta;
    state.obsidian += state.obsidian_robots * delta;
    state.geodes += state.geode_robots * delta;
}

fn when_will_there_be_enough(cur: u8, robots: u8, required: u8) -> u8 {
    if cur >= required {
        return 0;
    } else if robots == 0 {
        return u8::MAX;
    } else {
        let t = (required - cur + robots - 1) / robots;
        assert!(cur + (t * robots) >= required);
        assert!(t > 0);
        assert!(cur + ((t - 1) * robots) < required);
        return t;
    }
}

fn decision(cur_state: &State, costs: &Costs) -> u8 {
    // No more production if we ran out of time
    if cur_state.time_left == 0 {
        return cur_state.geodes;
    }

    // What can we do next?
    let ore_robot_delay = when_will_there_be_enough(cur_state.ore, cur_state.ore_robots, costs.ore_robot_ore_cost);
    let clay_robot_delay = when_will_there_be_enough(cur_state.ore, cur_state.ore_robots, costs.clay_robot_ore_cost);
    let obsidian_robot_delay = u8::max(
        when_will_there_be_enough(cur_state.ore, cur_state.ore_robots, costs.obsidian_robot_ore_cost),
        when_will_there_be_enough(cur_state.clay, cur_state.clay_robots, costs.obsidian_robot_clay_cost));
    let geode_robot_delay = u8::max(
        when_will_there_be_enough(cur_state.ore, cur_state.ore_robots, costs.geode_robot_ore_cost),
        when_will_there_be_enough(cur_state.obsidian, cur_state.obsidian_robots, costs.geode_robot_obsidian_cost));

    // If we can make a geode robot, don't need to do anything else
    if geode_robot_delay == 0 {
        let mut next_state: State = *cur_state;
        advance_state(&mut next_state, 1);
        next_state.geode_robots += 1;
        next_state.ore -= costs.geode_robot_ore_cost;
        next_state.obsidian -= costs.geode_robot_obsidian_cost;
        return decision(&next_state, costs);
    }

    // Pick one and do it
    let mut best_geodes: u8 = cur_state.geodes + (cur_state.time_left * cur_state.geode_robots);
    if ore_robot_delay < cur_state.time_left {
        let mut next_state: State = *cur_state;
        advance_state(&mut next_state, ore_robot_delay + 1);
        next_state.ore_robots += 1;
        next_state.ore -= costs.ore_robot_ore_cost;
        best_geodes = u8::max(best_geodes, decision(&next_state, costs));
    }
    if clay_robot_delay < cur_state.time_left {
        let mut next_state: State = *cur_state;
        advance_state(&mut next_state, clay_robot_delay + 1);
        next_state.clay_robots += 1;
        next_state.ore -= costs.clay_robot_ore_cost;
        best_geodes = u8::max(best_geodes, decision(&next_state, costs));
    }
    if obsidian_robot_delay < cur_state.time_left {
        let mut next_state: State = *cur_state;
        advance_state(&mut next_state, obsidian_robot_delay + 1);
        next_state.obsidian_robots += 1;
        next_state.ore -= costs.obsidian_robot_ore_cost;
        next_state.clay -= costs.obsidian_robot_clay_cost;
        best_geodes = u8::max(best_geodes, decision(&next_state, costs));
    }
    if geode_robot_delay < cur_state.time_left {
        let mut next_state: State = *cur_state;
        advance_state(&mut next_state, geode_robot_delay + 1);
        next_state.geode_robots += 1;
        next_state.ore -= costs.geode_robot_ore_cost;
        next_state.obsidian -= costs.geode_robot_obsidian_cost;
        best_geodes = u8::max(best_geodes, decision(&next_state, costs));
    }
    return best_geodes;
}

fn evaluate(line_string: &str, total_time: u8) -> u8 {
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

    return decision(&State {
        ore: 0,
        clay: 0,
        obsidian: 0,
        geodes: 0,
        ore_robots: 1,
        clay_robots: 0,
        obsidian_robots: 0,
        geode_robots: 0,
        time_left: total_time,
    }, &costs);
}

#[test]
fn test_part1a() {
    assert_eq!(evaluate(&"Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.", 24), 9);
}

#[test]
fn test_part1b() {
    assert_eq!(evaluate(&"Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian.", 24), 12);
}

#[test]
fn test_part1c() {
    assert_eq!(evaluate(&"Blueprint 19: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 7 clay. Each geode robot costs 4 ore and 11 obsidian.", 24), 4);
}

fn part1(filename: &str) -> u32 {
    let file = File::open(filename).unwrap();
    let mut id: u32 = 0;
    let mut total: u32 = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            id += 1;
            let geodes = evaluate(line_string.as_str(), 24) as u32;
            total += id * geodes;
        }
    }
    return total;
}

fn part2(filename: &str) -> u32 {
    let file = File::open(filename).unwrap();
    let mut id: u32 = 0;
    let mut total: u32 = 1;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            id += 1;
            let geodes = evaluate(line_string.as_str(), 32) as u32;
            total *= geodes;
            if id >= 3 {
                break;
            }
        }
    }
    return total;
}

fn main() {
    println!("{}", part1(&"input"));
    println!("{}", part2(&"input"));
}


use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashSet;

struct Rule {
    from: String,
    to: String,
}

fn apply_rules(initial_state: &str, rules: &Vec<Rule>) -> HashSet<String> {
    // Produce new states
    let mut new_states: HashSet<String> = HashSet::new();
    for start_index in 0 .. initial_state.len() {
        for rule in rules {
            let end_index = start_index + rule.from.len();
            if end_index <= initial_state.len() {
                if initial_state[start_index .. end_index] == rule.from {
                    let mut new_state = initial_state[0 .. start_index].to_string();
                    new_state.push_str(&rule.to);
                    new_state.push_str(&initial_state[end_index .. initial_state.len()].to_string());
                    new_states.insert(new_state);
                }
            }
        }
    }
    return new_states;
}

fn main() {
    // Read rules
    let file = File::open("input").unwrap();
    let lines = io::BufReader::new(file).lines();
    let mut initial_state: String = String::new();
    let mut rules: Vec<Rule> = Vec::new();
    for line in lines {
        if let Ok(line_string) = line {
            let line_vec = Vec::from_iter(line_string.split_ascii_whitespace());

            if line_vec.len() == 3 {
                assert_eq!(line_vec[1], "=>");
                rules.push(Rule {
                    from: line_vec[0].to_string(),
                    to: line_vec[2].to_string(),
                });
            } else if line_vec.len() == 1 {
                initial_state = line_vec[0].to_string();
            } else {
                assert_eq!(line_vec.len(), 0);
            }
        }
    }
    assert_ne!(initial_state.len(), 0);
    assert_ne!(rules.len(), 0);

    // Produce new states
    let new_states = apply_rules(&initial_state, &rules);
    println!("{}", new_states.len());
}

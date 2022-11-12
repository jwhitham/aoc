
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashSet;

type Atom = u16;
type Molecule = Vec<Atom>;

fn convert_to_molecule(s: &str) -> Molecule {
    let mut molecule = Molecule::new();
    for ch in s.bytes() {
        let now: u16 = ch.into();
        if ch.is_ascii_uppercase() || molecule.is_empty() {
            molecule.push(now);
        } else {
            let previous = molecule.pop().unwrap();
            molecule.push((previous << 8) | now);
        }
    }
    return molecule;
}

struct Rule {
    from: Molecule,
    to: Molecule,
}

fn apply_rules(initial_state: &Molecule, rules: &Vec<Rule>) -> HashSet<Molecule> {
    // Produce new states
    let mut new_states: HashSet<Molecule> = HashSet::new();
    for start_index in 0 .. initial_state.len() {
        for rule in rules {
            let end_index = start_index + rule.from.len();
            if end_index <= initial_state.len() {
                if initial_state[start_index .. end_index] == rule.from {
                    let mut new_state = Vec::from(&initial_state[0 .. start_index]);
                    new_state.extend(&rule.to);
                    new_state.extend(&initial_state[end_index .. initial_state.len()]);
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
    let mut initial_state: Molecule = Vec::new();
    let mut rules: Vec<Rule> = Vec::new();
    for line in lines {
        if let Ok(line_string) = line {
            let line_vec = Vec::from_iter(line_string.split_ascii_whitespace());

            if line_vec.len() == 3 {
                assert_eq!(line_vec[1], "=>");
                rules.push(Rule {
                    from: convert_to_molecule(line_vec[0]),
                    to: convert_to_molecule(line_vec[2]),
                });
            } else if line_vec.len() == 1 {
                initial_state = convert_to_molecule(line_vec[0]);
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

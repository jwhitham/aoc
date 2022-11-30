
use std::fs::File;
use std::io::{self, BufRead};

const MAX_COMPARTMENTS: usize = 4;

struct Best {
    compartment_1_size: usize,
    compartment_1_qe: f64,
}

struct State {
    todo: Vec<usize>,
    selected_for: [Vec<usize>; MAX_COMPARTMENTS + 1],
    not_selected_for: [Vec<usize>; MAX_COMPARTMENTS + 1],
    compartment_weight: [usize; MAX_COMPARTMENTS + 1],
    compartment_qe: [f64; MAX_COMPARTMENTS + 1],
    compartment_number: usize,
    num_compartments: usize,
    best: Best,
}

// Compute QE value
fn compute_qe(selected: &Vec<usize>) -> f64 {
    let mut total: f64 = 1.0;
    for value in selected.iter() {
        let v: usize = *value;
        total *= v as f64;
    }
    return total;
}

// Select for compartment [1 .. num_compartments - 1]
fn do_select(state: &mut State) {

    let number = state.compartment_number;
    if number == 1 {
        // Compartment 1 special case
        if state.selected_for[number].len() > state.best.compartment_1_size {
            // too many items here
            return;
        }
        if state.compartment_qe[number] > state.best.compartment_1_qe {
            // too much QE here
            return;
        }
    }

    if state.compartment_weight[number] == 0 {
        // can't add more items here now - go to next compartment
        if (state.compartment_qe[number] <= state.compartment_qe[1]) && (number > 1) {
            // QE of compartment 1 would be too large with this solution
            return;
        }
        if number == (state.num_compartments - 1) {
            // All compartments apart from the last one are now full - solution found
            state.compartment_qe[number + 1] = compute_qe(&state.not_selected_for[number]);
            if state.compartment_qe[number + 1] <= state.compartment_qe[1] {
                // QE of compartment 1 would be too large with this solution
                return;
            }
            // otherwise the solution should be valid - check
            for i in 1 .. state.num_compartments {
                assert_eq!(state.compartment_qe[i], compute_qe(&state.selected_for[i]));
            }
            for i in 2 .. (state.num_compartments + 1) {
                assert!(state.compartment_qe[i] > state.compartment_qe[1]);
            }
            assert!(state.best.compartment_1_size >= state.selected_for[1].len());
            state.best.compartment_1_size = state.selected_for[1].len();
            state.best.compartment_1_qe = f64::min(state.compartment_qe[1],
                                                   state.best.compartment_1_qe);
        } else {
            // unselected items from this compartment re-enter the todo list
            let saved_len = state.todo.len();
            for weight in state.not_selected_for[number].iter() {
                state.todo.push(*weight);
            }
            state.compartment_number += 1;
            do_select(state);
            state.compartment_number -= 1;
            state.todo.truncate(saved_len);
        }
        return;
    }

    if state.todo.len() == 0 {
        // We should never have selected the final item as all compartments
        // must contain at least 1 item
        return;
    }

    // get next item for selection
    let weight = state.todo.pop().unwrap();

    if weight <= state.compartment_weight[number] {
        // did select
        let saved_qe = state.compartment_qe[number];
        state.compartment_weight[number] -= weight;
        state.compartment_qe[number] *= weight as f64;
        state.selected_for[number].push(weight);
        do_select(state);
        state.selected_for[number].pop();
        state.compartment_qe[number] = saved_qe;
        state.compartment_weight[number] += weight;
    }
    // did not select
    state.not_selected_for[number].push(weight);
    do_select(state);
    state.not_selected_for[number].pop();

    // restore todo list
    state.todo.push(weight);
}


fn solver(num_compartments: usize) {
    // read input
    let file = File::open("input").unwrap();
    let lines = io::BufReader::new(file).lines();
    let mut weight: Vec<usize> = Vec::new();
    for line in lines {
        if let Ok(line_string) = line {
            weight.push(line_string.trim().parse().unwrap());
        }
    }
   
    // each compartment should have a specific weight, a proportion of the total
    let mut total: usize = 0;
    for w in &weight {
        total += w;
    }
    assert!((total % 3) == 0);
    assert!(num_compartments <= MAX_COMPARTMENTS);
    assert!(num_compartments >= 3);

    // begin solving
    let mut state = State {
        todo: weight,
        selected_for: Default::default(),
        not_selected_for: Default::default(),
        compartment_weight: [total / num_compartments; MAX_COMPARTMENTS + 1],
        compartment_qe: [1.0; MAX_COMPARTMENTS + 1],
        best: Best {
            compartment_1_size: usize::MAX,
            compartment_1_qe: f64::MAX,
        },
        num_compartments: num_compartments,
        compartment_number: 1,
    };
    do_select(&mut state);

    println!("{}", state.best.compartment_1_qe);
}

fn main() {
    solver(3);
    solver(4);
}


use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::convert::TryInto;

struct Best {
    compartment_1_size: usize,
    compartment_1_qe: f64,
}

struct State {
    todo: Vec<usize>,
    selected_for_1: Vec<usize>,
    selected_for_2: Vec<usize>,
    selected_for_3: Vec<usize>,
    not_selected_for_1: Vec<usize>,
    not_selected_for_2: Vec<usize>,
    compartment_1_weight: usize,
    compartment_2_weight: usize,
    compartment_1_qe: f64,
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

// Select for the first compartment
fn do_select_for_first(state: &mut State) {
    // finished selecting for first?
    if state.selected_for_1.len() > state.best.compartment_1_size {
        // too many items here
        return;
    }
    if state.compartment_1_qe > state.best.compartment_1_qe {
        // too much QE here
        return;
    }
    if state.compartment_1_weight == 0 {
        // can't add more items here now - go to second compartment
        // unselected items from compartment 1 re-enter the todo list
        let transfer_len = state.not_selected_for_1.len();
        for _ in 0 .. transfer_len {
            state.todo.push(state.not_selected_for_1.pop().unwrap());
        }
        do_select_for_second(state);
        for _ in 0 .. transfer_len {
            state.not_selected_for_1.push(state.todo.pop().unwrap());
        }
        return;
    }

    // nothing for compartment 2 or 3?
    if state.todo.len() == 0 {
        return;
    }

    // get next item for selection
    let weight = state.todo.pop().unwrap();

    if weight <= state.compartment_1_weight {
        // did select
        let saved_qe = state.compartment_1_qe;
        state.compartment_1_weight -= weight;
        state.compartment_1_qe *= weight as f64;
        state.selected_for_1.push(weight);
        do_select_for_first(state);
        state.selected_for_1.pop();
        state.compartment_1_qe = saved_qe;
        state.compartment_1_weight += weight;
    }
    // did not select
    state.not_selected_for_1.push(weight);
    do_select_for_first(state);
    state.not_selected_for_1.pop();

    // restore todo list
    state.todo.push(weight);
}

// Select for the second compartment
fn do_select_for_second(state: &mut State) {
    // finished selecting for second?
    if state.compartment_2_weight == 0 {
        state.best.compartment_1_size = state.selected_for_1.len();
        let qe_1 = compute_qe(&state.selected_for_1);
        let qe_2 = compute_qe(&state.selected_for_2);
        let qe_3 = compute_qe(&state.selected_for_3);
        assert_eq!(qe_1, state.compartment_1_qe);
        if (qe_1 < qe_2) && (qe_1 < qe_3) {
            // solution is acceptable
            state.best.compartment_1_qe = f64::min(qe_1, state.best.compartment_1_qe);
        }
        return;
    }

    // nothing for compartment 3?
    if state.todo.len() == 0 {
        return;
    }

    // get next item for selection
    let weight = state.todo.pop().unwrap();

    if weight <= state.compartment_2_weight {
        // did select
        state.compartment_2_weight -= weight;
        state.selected_for_2.push(weight);
        do_select_for_second(state);
        state.selected_for_2.pop();
        state.compartment_2_weight += weight;
    }
    // did not select
    state.selected_for_3.push(weight);
    do_select_for_second(state);
    state.selected_for_3.pop();

    // restore todo list
    state.todo.push(weight);
}


fn main() {
    // read input
    let file = File::open("input").unwrap();
    let lines = io::BufReader::new(file).lines();
    let mut weight: Vec<usize> = Vec::new();
    for line in lines {
        if let Ok(line_string) = line {
            weight.push(line_string.trim().parse().unwrap());
        }
    }
    
    // each compartment should have a specific weight, a third of the total
    let mut total: usize = 0;
    for w in &weight {
        total += w;
    }
    assert!((total % 3) == 0);
    let third = total / 3;

    // begin solving
    let mut state = State {
        todo: weight,
        selected_for_1: Vec::new(),
        selected_for_2: Vec::new(),
        selected_for_3: Vec::new(),
        not_selected_for_1: Vec::new(),
        not_selected_for_2: Vec::new(),
        compartment_1_weight: third,
        compartment_2_weight: third,
        compartment_1_qe: 1.0,
        best: Best {
            compartment_1_size: usize::MAX,
            compartment_1_qe: f64::MAX,
        }
    };
    do_select_for_first(&mut state);

    println!("{}", state.best.compartment_1_qe);
}

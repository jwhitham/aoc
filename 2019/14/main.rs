
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;
use std::collections::HashMap;

type Quantity = i32;
type Identifier = u8;

struct Molecule {
    quantity: Quantity,
    id: Identifier,
}

struct Reaction {
    inputs: Vec<Molecule>,
    output: Molecule,
}

type Reactions = Vec<Reaction>;

struct Problem {
    reactions: Reactions,
    ore_id: Identifier,
    fuel_id: Identifier,
}

fn load_values(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut reactions: Reactions = Vec::new();
    let mut name_to_id: HashMap<String, Identifier> = HashMap::new();
    let mut get_id = |name: &str| -> Identifier {
        let id = name_to_id.get(name);
        if id.is_some() {
            return *id.unwrap();
        } else {
            let new_id = name_to_id.len() as Identifier;
            name_to_id.insert(name.to_string(), new_id);
            return new_id;
        }
    };

    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let cleaned = line_string.replace("=>", " ")
                                     .replace(",", " ");
            let fields = Vec::from_iter(cleaned.split_ascii_whitespace());
            let num_inputs = (fields.len() / 2) - 1;
            let mut get_molecule = |d: usize| -> Molecule {
                return Molecule {
                    quantity: fields.get(d * 2).unwrap().parse().expect("quantity"),
                    id: get_id(fields.get((d * 2) + 1).unwrap()),
                };
            };
            let output = get_molecule(num_inputs);
            let output_id = output.id;

            // reactions.get(output_id) will represent all reactions producing this output
            // need to extend the reactions vector accordingly
            while reactions.len() <= (output_id as usize) {
                reactions.push(Reaction {
                    inputs: Vec::new(),
                    output: Molecule {
                        quantity: 0,
                        id: 0,
                    },
                });
            }

            let mut reaction = reactions.get_mut(output_id as usize).unwrap();
            reaction.output = output;
            for d in 0 .. num_inputs {
                reaction.inputs.push(get_molecule(d));
            }
        }
    }

    let ore_id = get_id("ORE");
    let fuel_id = get_id("FUEL");
    return Problem {
        reactions: reactions,
        ore_id: ore_id,
        fuel_id: fuel_id,
    }
}

fn make_more(problem: &Problem, unused: &mut Vec<Quantity>, output_id: Identifier, output_qty: Quantity) -> Quantity {
    assert!(output_qty > 0);

    // Generate ore as required
    if output_id == problem.ore_id {
        return output_qty;
    }

    // For everything else, use from the unused pile first
    let unused_qty_before: Quantity = *unused.get(output_id as usize).unwrap();
    let unused_qty_after: Quantity = Quantity::max(unused_qty_before - output_qty, 0);
    *unused.get_mut(output_id as usize).unwrap() = unused_qty_after;

    let needed_qty = output_qty - (unused_qty_before - unused_qty_after);
    if needed_qty == 0 {
        // Nothing more is needed
        return 0;
    }
    assert!(needed_qty > 0);
    assert!(unused_qty_after == 0);

    // Generate more
    let reaction = problem.reactions.get(output_id as usize).unwrap();
    let repeats = (reaction.output.quantity + needed_qty - 1) / reaction.output.quantity;
    assert!(repeats > 0);
    assert!((reaction.output.quantity * repeats) >= needed_qty);
    let mut ore = 0;
    for input in reaction.inputs.iter() {
        ore += make_more(problem, unused, input.id, input.quantity * repeats);
    }

    // anything unused goes on the unused pile
    let unused_qty_after_2: Quantity = (reaction.output.quantity * repeats) - needed_qty;
    *unused.get_mut(output_id as usize).unwrap() = unused_qty_after_2;

    return ore;
}

fn part1(filename: &str) -> Quantity {

    let problem = load_values(filename);
    let mut unused = Vec::new();
    while unused.len() < problem.reactions.len() {
        unused.push(0);
    }
    return make_more(&problem, &mut unused, problem.fuel_id, 1);
}

#[test]
fn test_part1() {
    assert_eq!(part1("test165"), 165);
}

#[test]
fn test_part1a() {
    assert_eq!(part1("test13312"), 13312);
}

#[test]
fn test_part1b() {
    assert_eq!(part1("test180697"), 180697);
}

#[test]
fn test_part1c() {
    assert_eq!(part1("test2210736"), 2210736);
}

fn main() {
    println!("{}", part1("input"));
}



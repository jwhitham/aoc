
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

type ReactionsForOutputIdentifier = Vec<Reaction>;
type Reactions = Vec<ReactionsForOutputIdentifier>;

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
                reactions.push(Vec::new());
            }

            let mut reaction = Reaction {
                inputs: Vec::new(),
                output: output,
            };
            for d in 0 .. num_inputs {
                reaction.inputs.push(get_molecule(d));
            }
            reactions.get_mut(output_id as usize).unwrap().push(reaction);
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


fn part1(filename: &str) -> Quantity {
    let problem = load_values(filename);
    return problem.ore_id as Quantity;
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



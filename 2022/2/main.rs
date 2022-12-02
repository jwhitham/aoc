
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;


#[derive(Eq, PartialEq)]
enum Outcome { DRAW, WIN, LOSE }

fn get_outcome(opponent_move: &str, my_move: &str) -> Outcome {
    return match opponent_move {
        "A" => match my_move {
            "A" | "X" => Outcome::DRAW,
            "B" | "Y" => Outcome::WIN,
            "C" | "Z" => Outcome::LOSE,
            _ => panic!(),
        },
        "B" => match my_move {
            "A" | "X" => Outcome::LOSE,
            "B" | "Y" => Outcome::DRAW,
            "C" | "Z" => Outcome::WIN,
            _ => panic!(),
        },
        "C" => match my_move {
            "A" | "X" => Outcome::WIN,
            "B" | "Y" => Outcome::LOSE,
            "C" | "Z" => Outcome::DRAW,
            _ => panic!(),
        },
        _ => panic!(),
    };
}

fn get_score(opponent_move: &str, my_move: &str) -> u32 {
    let result_score = match get_outcome(opponent_move, my_move) {
        Outcome::WIN => 6,
        Outcome::DRAW => 3,
        Outcome::LOSE => 0,
    };
    let shape_score = match my_move {
        "A" | "X" => 1,
        "B" | "Y" => 2,
        "C" | "Z" => 3,
        _ => panic!(),
    };
    return shape_score + result_score;
}

fn get_move(opponent_move: &str, outcome_code: &str) -> String {
    let outcome = match outcome_code {
        "X" => Outcome::LOSE,
        "Y" => Outcome::DRAW,
        "Z" => Outcome::WIN,
        _ => panic!(),
    };
    for try_move in ["A", "B", "C"] {
        if get_outcome(opponent_move, try_move) == outcome {
            return try_move.to_string();
        }
    }
    panic!();
}

fn main() {
    let file = File::open("input").unwrap();
    let mut part1_total: u32 = 0;
    let mut part2_total: u32 = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let fields = Vec::from_iter(line_string.split_ascii_whitespace());
            assert_eq!(fields.len(), 2);
            part1_total += get_score(fields[0], fields[1]);
            let choice = get_move(fields[0], fields[1]);
            part2_total += get_score(fields[0], choice.as_str());
        }
    }

    println!("{}", part1_total);
    println!("{}", part2_total);
}

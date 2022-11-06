
use std::fs::File;
use std::io::{self, BufRead};

use std::iter::FromIterator;

struct Reindeer {
    // name: String,
    fly_speed: usize,
    fly_time: usize,
    rest_time: usize,
    position: usize,
    resting: bool,
    remaining_time: usize,
    score: usize,
}

fn move_all_reindeer(reindeer: &mut Vec<Reindeer>) {
    for r in reindeer {
        if r.remaining_time == 0 {
            if r.resting {
                r.resting = false;
                r.remaining_time = r.fly_time;
            } else {
                r.resting = true;
                r.remaining_time = r.rest_time;
            }
        }
        if !r.resting {
            r.position += r.fly_speed;
        }
        r.remaining_time -= 1;
    }
}

fn main() {
    // Read input
    let file = File::open("input").unwrap();
    let lines = io::BufReader::new(file).lines();
    let mut reindeer: Vec<Reindeer> = Vec::new();
    for line in lines {
        if let Ok(line_string) = line {
            let line_vec = Vec::from_iter(line_string.split(' '));
            reindeer.push(Reindeer {
                // name: line_vec[0].to_string(),
                fly_speed: line_vec[3].parse().unwrap(),
                fly_time: line_vec[6].parse().unwrap(),
                rest_time: line_vec[13].parse().unwrap(),
                position: 0,
                resting: true,
                remaining_time: 0,
                score: 0,
            });
        }
    }

    // Part 1
    for _ in 0 .. 2503 {
        move_all_reindeer(&mut reindeer);
    }
    let mut furthest_position: usize = 0;
    for r in &reindeer {
        if furthest_position < r.position {
            furthest_position = r.position;
        }
    }
    println!("{}", furthest_position);

    // Reset for part 2
    for r in &mut reindeer {
        r.position = 0;
        r.resting = true;
        r.remaining_time = 0;
    }

    // Part 2
    for _ in 0 .. 2503 {
        move_all_reindeer(&mut reindeer);
        furthest_position = 0;
        for r in &reindeer {
            if furthest_position < r.position {
                furthest_position = r.position;
            }
        }
        for r in &mut reindeer {
            if furthest_position == r.position {
                r.score += 1;
            }
        }
    }
    let mut highest_score: usize = 0;
    for r in &reindeer {
        if highest_score < r.score {
            highest_score = r.score;
        }
    }
    println!("{}", highest_score);
}


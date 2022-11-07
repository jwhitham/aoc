
use std::fs::File;
use std::io::{self, BufRead};

fn count_permutations(containers: &Vec<u32>, limit: usize, eggnog_left: u32, containers_left: usize) -> u32 {
    if eggnog_left == 0 {
        // base case: no eggnog
        return 1;
    }
    if containers_left == 0 {
        // base case: no more containers
        return 0;
    }
    let mut count: u32 = 0;
    for i in 0 .. limit {
        let size = containers[i];
        if size <= eggnog_left {
            // This container can be picked - search onwards
            count += count_permutations(containers, i, eggnog_left - size, containers_left - 1);
        }
    }
    return count;
}

fn main() {
    // Read input (container sizes)
    let file = File::open("input").unwrap();
    let lines = io::BufReader::new(file).lines();
    let mut containers: Vec<u32> = Vec::new();
    for line in lines {
        if let Ok(line_string) = line {
            let parsed = line_string.parse();
            let value: u32 = parsed.unwrap();
            containers.push(value);
        }
    }
    containers.sort();

    // Part 1
    let count = count_permutations(&containers, containers.len(), 150, containers.len());
    println!("{}", count);

    // Part 2
    for num_containers in 1 .. containers.len() {
        let count = count_permutations(&containers, containers.len(), 150, num_containers);
        if count != 0 {
            println!("{}", count);
            break;
        }
    }
}

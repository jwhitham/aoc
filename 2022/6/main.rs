
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::VecDeque;
use std::collections::HashMap;

fn main() {
    let file = File::open("input").unwrap();
    let line = io::BufReader::new(file).lines().next().unwrap();
    let mut delay: VecDeque<char> = VecDeque::new();
    let mut ch_count: HashMap<char, u32> = HashMap::new();
    let mut rx_count: u32 = 0;

    for new_ch in line.expect("ok").chars() {
        delay.push_back(new_ch);
        ch_count.insert(new_ch, ch_count.get(&new_ch).unwrap_or(&0) + 1);
        rx_count += 1;

        if rx_count > 4 {
            assert_eq!(delay.len(), 5);
            let old_ch = delay.pop_front().unwrap();
            ch_count.insert(old_ch, ch_count.get(&old_ch).unwrap() - 1);

            let mut repeat = false;
            for value in ch_count.values() {
                if *value > 1 {
                    repeat = true;
                    break;
                }
            }
            if !repeat {
                println!("{}", rx_count);
                break;
            }
        }
    }
}


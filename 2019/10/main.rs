
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;
//use std::hash::{Hash, Hasher};


type Word = i8;

#[derive(Hash, Eq, PartialEq)]
struct Asteroid {
    x: Word,
    y: Word,
}

/*
impl Hash for Asteroid {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.x.hash(state);
        self.y.hash(state);
    }
}
*/

fn greatest_common_divisor(a: Word, b: Word) -> Word {
    let mut copy_a = a;
    let mut copy_b = b;
    loop {
        copy_a %= copy_b;
        if copy_a == 0 {
            return copy_b;
        }
        copy_b %= copy_a;
        if copy_b == 0 {
            return copy_a;
        }
    }
}


fn part1(filename: &str) -> u32 {
    let file = File::open(filename).unwrap();
    let mut y: Word = 0;
    let mut x: Word = 0;
    let mut asteroid_set: HashSet<Asteroid> = HashSet::new();
    let mut asteroid_list: Vec<Asteroid> = Vec::new();
    for line in io::BufReader::new(file).lines() {
        x = 0;
        if let Ok(line_string) = line {
            for ch in line_string.chars() {
                if ch == '#' {
                    asteroid_set.insert(Asteroid { x: x, y: y });
                    asteroid_list.push(Asteroid { x: x, y: y });
                }
                x += 1;
            }
        }
        y += 1;
    }
    let width = x;
    let height = y;
    let mut best_visible_count: u32 = 0;
    for centre in &asteroid_list {
        // Count visible asteroids if the monitoring station is at centre
        let mut visible_count: u32 = 0;
        //println!("try {},{}", centre.x, centre.y);
        for asteroid in &asteroid_list {
            // Here's the vector to the asteroid
            let mut dx = asteroid.x - centre.x;
            let mut dy = asteroid.y - centre.y;
            if dx == 0 {
                // The asteroid is directly along a vertical line
                if dy == 0 {
                    // Trivially visible! (same place)
                } else if dy > 0 {
                    dy = 1;
                } else {
                    dy = -1;
                }
            } else if dy == 0 {
                // The asteroid is directly along a horizontal line
                if dx > 0 {
                    dx = 1;
                } else {
                    dx = -1;
                }
            } else {
                // Reduce the vector to the smallest equivalent
                let divide_by = Word::abs(greatest_common_divisor(dx, dy));
                assert!((dx % divide_by) == 0);
                assert!((dy % divide_by) == 0);
                dx /= divide_by;
                dy /= divide_by;
            }
            //println!("  test {},{}  d {},{}", asteroid.x, asteroid.y, dx, dy);
            // Step to the asteroid
            let mut sx = centre.x + dx;
            let mut sy = centre.y + dy;
            let mut visible = true;
            while (sx != asteroid.x) || (sy != asteroid.y) {
                assert!((dx != 0) || (dy != 0));
                assert!(sx >= 0);
                assert!(sy >= 0);
                assert!(sx < width);
                assert!(sy < height);
                if asteroid_set.contains(&Asteroid { x: sx, y: sy }) {
                    // The view is blocked!
                    visible = false;
                    //println!("  blocked at {},{}", sx, sy);
                    break;
                }
                sx += dx;
                sy += dy;
            }
            if visible {
                // println!("  not blocked");
                visible_count += 1;
            }
        }
        // Can't see what you're standing on:
        visible_count -= 1;
        // println!("  count for {},{} is {}", centre.x, centre.y, visible_count);
        if visible_count > best_visible_count {
            best_visible_count = visible_count;
        }
    }
    return best_visible_count;
}

#[test]
fn test_part1() {
    assert_eq!(part1("test8"), 8);
    assert_eq!(part1("test33"), 33);
    assert_eq!(part1("test210"), 210);
}

fn main() {
    println!("{}", part1("input"));
}



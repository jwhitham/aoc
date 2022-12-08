
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;


type Word = i8;

#[derive(Hash, Eq, PartialEq)]
struct Asteroid {
    x: Word,
    y: Word,
}

fn greatest_common_divisor(a: Word, b: Word) -> Word {
    if a == 0 {
        return b;
    } else if b == 0 {
        return a;
    }
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
    for line in io::BufReader::new(file).lines() {
        x = 0;
        if let Ok(line_string) = line {
            for ch in line_string.chars() {
                if ch == '#' {
                    asteroid_set.insert(Asteroid { x: x, y: y });
                }
                x += 1;
            }
        }
        y += 1;
    }
    let width = x;
    let height = y;
    let mut best_visible_count: u32 = 0;
    for centre in &asteroid_set {
        // Count visible asteroids if the monitoring station is at centre
        let mut visible_count: u32 = 0;
        for asteroid in &asteroid_set {
            // Here's the vector to the asteroid
            let mut dx = asteroid.x - centre.x;
            let mut dy = asteroid.y - centre.y;
            if dx == 0 && dy == 0 {
                // Same place - does not count as visible
                continue;
            }
            // Reduce the vector to the smallest equivalent
            let divide_by = Word::abs(greatest_common_divisor(dx, dy));
            assert!((dx % divide_by) == 0);
            assert!((dy % divide_by) == 0);
            dx /= divide_by;
            dy /= divide_by;

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
                    break;
                }
                sx += dx;
                sy += dy;
            }
            if visible {
                visible_count += 1;
            }
        }
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



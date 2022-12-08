
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


fn main() {
    let file = File::open("input").unwrap();
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
    for cy in 0 .. height {
        for cx in 0 .. width {
            // Count visible asteroids if the monitoring station is at cx, cy
            let mut visible_count: u32 = 0;
            for asteroid in &asteroid_list {
                // Here's the vector to the asteroid
                let mut dx = asteroid.x - cx;
                let mut dy = asteroid.y - cy;
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
                // Step to the asteroid
                let mut sx = cx + dx;
                let mut sy = cy + dy;
                let mut visible = true;
                while (sx != asteroid.x) && (sy != asteroid.y) {
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
    }
    println!("{}", best_visible_count);
}


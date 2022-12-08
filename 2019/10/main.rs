
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;
use std::collections::HashMap;
use std::cmp::Ordering;


type Word = i8;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
struct Asteroid {
    x: Word,
    y: Word,
}

type AsteroidSet = HashSet<Asteroid>;

struct Problem {
    asteroid_set: AsteroidSet,
    width: Word,
    height: Word,
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

fn load_file(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut y: Word = 0;
    let mut x: Word = 0;
    let mut asteroid_set: AsteroidSet = HashSet::new();
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
    return Problem {
        asteroid_set: asteroid_set,
        width: x,
        height: y,
    };
}

fn find_best_asteroid(problem: &Problem) -> (u32, Asteroid) {
    let mut best_visible_count: u32 = 0;
    let mut best_location = Asteroid { x: 0, y: 0 };
    for centre in &problem.asteroid_set {
        // Count visible asteroids if the monitoring station is at centre
        let mut visible_count: u32 = 0;
        for asteroid in &problem.asteroid_set {
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
                assert!(sx < problem.width);
                assert!(sy < problem.height);
                if problem.asteroid_set.contains(&Asteroid { x: sx, y: sy }) {
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
            best_location = *centre;
        }
    }
    return (best_visible_count, best_location);
}

fn part1(filename: &str) -> u32 {
    let (c, _) = find_best_asteroid(&load_file(filename));
    return c;
}

#[test]
fn test_part1() {
    let mut c = part1("test8");
    assert_eq!(c, 8);
    c = part1("test33");
    assert_eq!(c, 33);
    c = part1("test210");
    assert_eq!(c, 210);
}

fn part2(filename: &str, index: usize) -> Asteroid {
    let problem = load_file(filename);
    let (_, source) = find_best_asteroid(&problem);

    #[derive(Hash, Eq, PartialEq, Copy, Clone)]
    struct DirectionVector {
        dx: Word,
        dy: Word,
    }

    struct Target {
        distance: f64,
        asteroid: Asteroid,
    }

    struct Direction {
        angle: f64,
        targets: Vec<Target>,
    }

    impl Eq for Direction {}

    impl PartialEq for Direction {
        fn eq(&self, other: &Self) -> bool {
            return self.cmp(other) == Ordering::Equal;
        }
    }

    impl PartialOrd for Direction {
        fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
            return Some(self.cmp(other));
        }
    }

    impl Ord for Direction {
        fn cmp(&self, other: &Self) -> Ordering {
            if self.angle < other.angle {
                return Ordering::Less;
            } else if self.angle > other.angle {
                return Ordering::Greater;
            } else {
                return Ordering::Equal;
            }
        }
    }

    impl Eq for Target {}

    impl PartialEq for Target {
        fn eq(&self, other: &Self) -> bool {
            return self.cmp(other) == Ordering::Equal;
        }
    }

    impl PartialOrd for Target {
        fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
            return Some(self.cmp(other));
        }
    }

    impl Ord for Target {
        fn cmp(&self, other: &Self) -> Ordering {
            if self.distance < other.distance {
                return Ordering::Less;
            } else if self.distance > other.distance {
                return Ordering::Greater;
            } else {
                return Ordering::Equal;
            }
        }
    }


    // Sort targets according to the smallest equivalent direction vector
    let mut by_direction_vector: HashMap<DirectionVector, Direction> = HashMap::new();
    for asteroid in &problem.asteroid_set {
        // Integer direction vector
        let mut dx = asteroid.x - source.x;
        let mut dy = asteroid.y - source.y;
        if (dx == 0) && (dy == 0) {
            continue;
        }

        // Calculate distance
        let dxf = dx as f64;
        let dyf = dy as f64;
        let distance = ((dxf * dxf) + (dyf * dyf)).sqrt();

        // Reduce the integer direction vector to the smallest equivalent
        let divide_by = Word::abs(greatest_common_divisor(dx, dy));
        assert!((dx % divide_by) == 0);
        assert!((dy % divide_by) == 0);
        dx /= divide_by;
        dy /= divide_by;

        let v = DirectionVector { dx: dx, dy: dy };
        let mut d = by_direction_vector.get_mut(&v);

        if d.is_none() {
            // Get the angle
            // angle 0 is directly up (dx = 0, dy = -1)
            // angle pi*0.5 is directly right
            // angle pi is directly down
            // angle pi*1.5 is directly left
            let dxf = v.dx as f64;
            let dyf = v.dy as f64;
            let mut angle = dxf.atan2(-dyf);
            if angle < 0.0 {
                angle += std::f64::consts::PI * 2.0;
            }
            by_direction_vector.insert(v, Direction {
                angle: angle,
                targets: Vec::new(),
            });
            d = by_direction_vector.get_mut(&v);
        }

        d.unwrap().targets.push(Target {
            distance: distance,
            asteroid: *asteroid,
        });
    }

    // Collect directions
    let mut by_direction: Vec<Direction> = by_direction_vector.into_values().collect();

    // Sort by angle
    by_direction.sort();

    // Within each direction vector, sort the targets by distance
    for d in by_direction.iter_mut() {
        d.targets.sort();
        d.targets.reverse();
    }

    // Zap those asteroids
    let mut count = index;
    loop {
        assert!(count > 0);
        let mut progress = false;
        for d in by_direction.iter_mut() {
            if !d.targets.is_empty() {
                let asteroid = d.targets.pop().unwrap().asteroid;
                count -= 1;
                progress = true;
                if count == 0 {
                    return asteroid;
                }
            }
        }
        assert!(progress);
    }
}

#[test]
fn test_part2() {
    let mut a = part2("test210", 1);
    assert_eq!(a.x, 11);
    assert_eq!(a.y, 12);
    a = part2("test210", 2);
    assert_eq!(a.x, 12);
    assert_eq!(a.y, 1);
    a = part2("test210", 3);
    assert_eq!(a.x, 12);
    assert_eq!(a.y, 2);
    a = part2("test210", 10);
    assert_eq!(a.x, 12);
    assert_eq!(a.y, 8);
    a = part2("test210", 20);
    assert_eq!(a.x, 16);
    assert_eq!(a.y, 0);
    a = part2("test210", 50);
    assert_eq!(a.x, 16);
    assert_eq!(a.y, 9);
    a = part2("test210", 100);
    assert_eq!(a.x, 10);
    assert_eq!(a.y, 16);
    a = part2("test210", 199);
    assert_eq!(a.x, 9);
    assert_eq!(a.y, 6);
    a = part2("test210", 200);
    assert_eq!(a.x, 8);
    assert_eq!(a.y, 2);
}


fn main() {
    let best_visible_count = part1("input");
    println!("{}", best_visible_count);
    let a = part2("input", 200);
    println!("{}", (a.x as usize * 100) + (a.y as usize));
}



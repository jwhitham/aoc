
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::BinaryHeap;
use std::cmp::Ordering;


#[derive(Copy, Clone)]
struct Location {
    x: usize,
    y: usize,
}

#[derive(Copy, Clone)]
struct HeapItem {
    location: Location,
    shortest: usize,
}

struct Cell {
    key: HeapItem,
    height: u8,
    previous: Location,
}

type Col = Vec<Cell>;
type Map = Vec<Col>;

struct Problem {
    map: Map,
    start: Location,
    end: Location,
}

impl Eq for HeapItem {}

impl PartialEq for HeapItem {
    fn eq(&self, other: &Self) -> bool {
        return self.cmp(other) == Ordering::Equal;
    }
}

impl PartialOrd for HeapItem {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        return Some(self.cmp(other));
    }
}

impl Ord for HeapItem {
    fn cmp(&self, other: &Self) -> Ordering {
        // Need a min-heap so the order is reversed
        if self.shortest > other.shortest {
            return Ordering::Less;
        } else if self.shortest < other.shortest {
            return Ordering::Greater;
        } else {
            return Ordering::Equal;
        }
    }
}


const NOWHERE: Location = Location { x: usize::MAX, y: usize::MAX };

fn load(filename: &str) -> Problem {
    let file = File::open(filename).unwrap();
    let mut p = Problem {
        map: Vec::new(),
        start: NOWHERE,
        end: NOWHERE,
    };

    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            p.map.push(Vec::new());
            for ch in line_string.trim().bytes() {
                let mut height: u8 = ch;
                let location = Location {
                    x: p.map.last().unwrap().len(),
                    y: p.map.len() - 1,
                };
                match ch {
                    b'S' => {
                        height = b'a';
                        p.start = location;
                    },
                    b'E' => {
                        height = b'z';
                        p.end = location;
                    },
                    _ => {},
                }
                p.map.last_mut().unwrap().push(Cell {
                    key: HeapItem {
                        location: location,
                        shortest: usize::MAX,
                    },
                    height: height,
                    previous: NOWHERE,
                });
            }
        }
    }
    return p;
}

fn shortest_path(p: &mut Problem) -> usize{
    let mut todo: BinaryHeap<HeapItem> = BinaryHeap::new();
    {
        let end: &mut Cell = p.map.get_mut(p.end.y).unwrap()
                                  .get_mut(p.end.x).unwrap();
                                    
        end.key.shortest = 0;
        todo.push(end.key);
    }

    while !todo.is_empty() {
        let sk: HeapItem = todo.pop().unwrap();
        assert!(sk.shortest < usize::MAX);

        let mut try_move = |dx: isize, dy: isize| {
            let tx = (sk.location.x as isize) + dx;
            let ty = (sk.location.y as isize) + dy;
            if (tx < 0) || (ty < 0)
            || (ty >= (p.map.len() as isize))
            || (tx >= (p.map.get(ty as usize).unwrap().len() as isize)) {
                // moves off the map
                return;
            }

            let shortest: usize;
            {
                let sc: &Cell = p.map.get(sk.location.y).unwrap()
                                     .get(sk.location.x).unwrap();
                let tc: &Cell = p.map.get(ty as usize).unwrap()
                                     .get(tx as usize).unwrap();
                if tc.height < (sc.height - 1) {
                    // too much of a height decreate
                    return;
                }
                assert!(sc.key.shortest < usize::MAX);
                assert!(sc.key.shortest == sk.shortest);
                shortest = sc.key.shortest + 1;
                if shortest >= tc.key.shortest {
                    // not a shorter path
                    return;
                }
            }
            {
                // shorter path found
                let tcm: &mut Cell = p.map.get_mut(ty as usize).unwrap()
                                          .get_mut(tx as usize).unwrap();
                tcm.key.shortest = shortest;
                tcm.previous = sk.location;
                todo.push(tcm.key);
            }
        };
        try_move(-1, 0);
        try_move(1, 0);
        try_move(0, -1);
        try_move(0, 1);
    }
    let start: &Cell = p.map.get(p.start.y).unwrap()
                            .get(p.start.x).unwrap();
    return start.key.shortest;
}

#[test]
fn test_part1() {
    assert_eq!(shortest_path(&mut load("test31")), 31);
}

fn main() {
    let mut p = load("input");
    println!("{}", shortest_path(&mut p));

    let mut sp = usize::MAX;
    for y in 0 .. p.map.len() {
        for x in 0 .. p.map.get(y).unwrap().len() {
            let cell = p.map.get(y).unwrap().get(x).unwrap();
            if cell.height == b'a' {
                sp = usize::min(sp, cell.key.shortest);
            }
        }
    }
    println!("{}", sp);
}



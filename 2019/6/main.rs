
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;
use std::rc::Rc;
use std::cell::RefCell;

struct Object {
    parent: Option<Rc<RefCell<Object>>>,
    flag: bool,
}

struct Space {
    object: HashMap<String, Rc<RefCell<Object>>>,
}

impl Space {
    fn new() -> Self {
        return Self {
            object: HashMap::new(),
        };
    }

    fn create(self: &mut Self, name: &str) {
        if !self.object.contains_key(name) {
            self.object.insert(name.to_string(), Rc::new(RefCell::new(Object {
                parent: None,
                flag: false,
            })));
        }
    }

    fn get(self: &Self, name: &str) -> Option<Rc<RefCell<Object>>> {
        return self.object.get(name).cloned();
    }

    fn parent(self: &Self, satellite: Rc<RefCell<Object>>) -> Option<Rc<RefCell<Object>>> {
        if let Some(planet) = &satellite.borrow().parent {
            return Some(planet.clone());
        }
        return None;
    }

    fn add_link(self: &mut Self,
                planet_name: &str, satellite_name: &str) {
        
        self.create(planet_name);
        self.create(satellite_name);
        if let Some(item1) = self.get(satellite_name) {
            let mut item2 = item1.borrow_mut();
            item2.parent = Some(self.get(planet_name).unwrap().clone());
        }
    }

    fn count_transitive(self: &mut Self) -> u32 {
        let mut count = 0;
        for satellite_name in self.object.keys() {
            if let Some(mut item1) = self.get(satellite_name) {
                while let Some(item2) = self.parent(item1) {
                    item1 = item2;
                    count += 1;
                }
            }
        }
        return count;
    }

    fn flip_flag(self: &mut Self, satellite_name: &str) -> u32 {
        let mut count = 0;
        if let Some(mut item1) = self.get(satellite_name) {
            while let Some(item2) = self.parent(item1) {
                {
                    let mut item3 = item2.borrow_mut();
                    if !item3.flag {
                        count += 1;
                        item3.flag = true;
                    } else {
                        item3.flag = false;
                    }
                }
                item1 = item2;
            }
        }
        return count;
    }
}

fn load_from_input() -> Space {
    let file = File::open("input").unwrap();
    let mut space = Space::new();
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            let mut pair = line_string.trim().split(')');
            let planet_name = pair.next().unwrap();
            let satellite_name = pair.next().unwrap();

            space.add_link(planet_name, satellite_name);
        }
    }
    return space;
}

fn part1() -> u32 {
    let mut space = load_from_input();
    return space.count_transitive();
}

fn part2() -> u32 {
    let mut space = load_from_input();
    let you_to_root = space.flip_flag("YOU");
    let santa_to_meeting = space.flip_flag("SAN");
    let meeting_to_root = space.flip_flag("YOU");
    let you_to_meeting = you_to_root - meeting_to_root;
    let you_to_santa = you_to_meeting + santa_to_meeting;
    return you_to_santa;
}

#[test]
fn test() {
    assert_eq!(139597, part1());
    assert_eq!(286, part2());
}

fn main() {
    println!("{}", part1());
    println!("{}", part2());
}


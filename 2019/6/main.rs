
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;


struct Object {
    parent: String,
    flag: bool,
}

struct Space {
    object: HashMap<String, Object>,
}

impl Space {
    fn new() -> Self {
        return Self {
            object: HashMap::new(),
        };
    }

    fn create(self: &mut Self, name: &str) {
        if !self.object.contains_key(name) {
            self.object.insert(name.to_string(), Object {
                parent: String::new(),
                flag: false,
            });
        }
    }

    fn get(self: &Self, name: &str) -> Option<&Object> {
        return self.object.get(name);
    }

    fn get_mut(self: &mut Self, name: &str) -> Option<&mut Object> {
        return self.object.get_mut(name);
    }

    fn parent_name(self: &Self, name: &str) -> Option<String> {
        return self.get(name).map(|item| item.parent.clone());
    }

    fn add_link(self: &mut Self,
                planet_name: &str, satellite_name: &str) {
        
        self.create(planet_name);
        self.create(satellite_name);
        if let Some(satellite) = self.get_mut(satellite_name) {
            satellite.parent = planet_name.to_string();
        }
    }

    fn count_transitive(self: &mut Self) -> u32 {
        let mut count = 0;
        for satellite_name in self.object.keys() {
            let mut name = self.parent_name(satellite_name);
            if name.is_some() {
                name = self.parent_name(&name.unwrap());
            }
            while name.is_some() {
                count += 1;
                name = self.parent_name(&name.unwrap());
            }
        }
        return count;
    }

    fn flip_flag(self: &mut Self, satellite_name: &str) -> u32 {
        let mut count = 0;
        let mut name = self.parent_name(satellite_name);
        while name.is_some() {
            if let Some(mut value) = self.get_mut(&name.unwrap()) {
                if !value.flag {
                    count += 1;
                    value.flag = true;
                } else {
                    value.flag = false;
                }
                name = Some(value.parent.clone());
            } else {
                name = None;
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


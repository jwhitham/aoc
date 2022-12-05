
use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;
use std::rc::Rc;
use std::cell::RefCell;


struct Object {
    parent: Option<Rc<RefCell<Object>>>,
    children: Vec<Rc<RefCell<Object>>>,
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

    fn get(self: &mut Self, name: &str) -> Rc<RefCell<Object>> {
        if let Some (obj) = self.object.get(name) {
            return obj.clone();
        }
        let new_obj = Rc::new(RefCell::new(Object {
            parent: None,
            children: Vec::new(),
        }));
        self.object.insert(name.to_string(), new_obj.clone());
        return new_obj;
    }

    fn add_link(self: &mut Self,
                planet_name: &str, satellite_name: &str) {
        
        let planet = self.get(planet_name);
        let satellite = self.get(satellite_name);
        assert!(satellite.borrow().parent.is_none());
        satellite.borrow_mut().parent = Some(planet.clone());
        planet.borrow_mut().children.push(satellite.clone());
    }

    fn count_transitive(self: &mut Self) -> u32 {
        let mut count = 0;
        for obj in self.object.values() {
            let mut step = obj.borrow().parent.clone();
            while step.is_some() {
                count += 1;
                step = step.unwrap().borrow().parent.clone();
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

fn part1() {
    let mut space = load_from_input();
    println!("{}", space.count_transitive());
}

fn main() {
    part1();
}


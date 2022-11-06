
use std::fs::File;
use std::io::{self, BufRead};
use std::iter::FromIterator;

struct Ingredient {
    //name: String,
    capacity: i32,
    durability: i32,
    flavor: i32,
    texture: i32,
    calories: i32,
    quantity: i32,
}

fn clamp(value: i32) -> i32 {
    if value < 0 {
        return 0;
    } else {
        return value;
    }
}

fn evaluate(ingredients: &Vec<Ingredient>) -> i32 {
    let mut capacity: i32 = 0;
    let mut durability: i32 = 0;
    let mut flavor: i32 = 0;
    let mut texture: i32 = 0;
    for ingredient in ingredients {
        capacity += ingredient.capacity * ingredient.quantity;
        durability += ingredient.durability * ingredient.quantity;
        flavor += ingredient.flavor * ingredient.quantity;
        texture += ingredient.texture * ingredient.quantity;
    }
    return clamp(capacity) * clamp(durability) * clamp(flavor) * clamp(texture);
}

fn find_best(ingredients: &mut Vec<Ingredient>, index: usize, quantity_left: i32) -> i32 {
    if index == (ingredients.len() - 1) {
        // Final ingredient
        ingredients[index].quantity = quantity_left;
        return evaluate(ingredients);
    }
    let mut best_overall = 0;
    for q in 0 .. quantity_left + 1 {
        ingredients[index].quantity = q;
        let best_here = find_best(ingredients, index + 1, quantity_left - q);
        if best_overall < best_here {
            best_overall = best_here;
        }
    }
    return best_overall;
}

fn find_best_with_calories(ingredients: &mut Vec<Ingredient>, index: usize,
                           quantity_left: i32, calories_left: i32) -> i32 {
    if index == (ingredients.len() - 1) {
        // Final ingredient
        let c = ingredients[index].calories * quantity_left;
        if c == calories_left {
            ingredients[index].quantity = quantity_left;
            return evaluate(ingredients);
        } else {
            return 0;
        }
    }
    let mut best_overall = 0;
    for q in 0 .. quantity_left + 1 {
        ingredients[index].quantity = q;
        let c = ingredients[index].calories * q;
        if c <= calories_left {
            let best_here = find_best_with_calories(ingredients, index + 1,
                                                    quantity_left - q, calories_left - c);
            if best_overall < best_here {
                best_overall = best_here;
            }
        }
    }
    return best_overall;
}


fn main() {
    // Read input
    let file = File::open("input").unwrap();
    let lines = io::BufReader::new(file).lines();
    let mut ingredients: Vec<Ingredient> = Vec::new();
    for line in lines {
        if let Ok(line_string) = line {
            let decomma = line_string.replace(",", "");
            let line_vec = Vec::from_iter(decomma.split_ascii_whitespace());
            ingredients.push(Ingredient {
                //name: line_vec[0].to_string(),
                capacity: line_vec[2].parse().unwrap(),
                durability: line_vec[4].parse().unwrap(),
                flavor: line_vec[6].parse().unwrap(),
                texture: line_vec[8].parse().unwrap(),
                calories: line_vec[10].parse().unwrap(),
                quantity: 0,
            });
        }
    }
    
    // Part 1
    let best_overall = find_best(&mut ingredients, 0, 100);
    println!("{}", best_overall);

    // Part 2
    let best_overall_with_calories = find_best_with_calories(&mut ingredients, 0, 100, 500);
    println!("{}", best_overall_with_calories);
}


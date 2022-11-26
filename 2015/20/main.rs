
const INPUT: u64 = 34000000;


use std::collections::BinaryHeap;
use std::cmp::Ordering;


#[derive(Eq, PartialEq)]
struct HeapItem {
    elf_number: u64,
    next_house: u64,
    deliveries_to_do: u64,
}

// The heap must be a "min heap" with the smallest value
// being the one which will be popped next. Rust's heap is
// actually a "max heap" so we flip the direction of the comparison.
impl Ord for HeapItem {
    fn cmp(self: &Self, other: &Self) -> Ordering {
        return other.next_house.cmp(&self.next_house);
    }
}

impl PartialOrd for HeapItem {
    fn partial_cmp(self: &Self, other: &Self) -> Option<Ordering> {
        return Some(self.cmp(other));
    }
}


fn solver(delivery_limit: u64, deliveries_per_house: u64) -> u64 {
    let mut heap: BinaryHeap<HeapItem> = BinaryHeap::new();
    let mut house_number = 1;

    loop {
        // add new elf
        heap.push(HeapItem {
            elf_number: house_number,
            next_house: house_number,
            deliveries_to_do: delivery_limit,
        });

        // count the number of presents being delivered here
        let mut sum_of_elf_numbers: u64 = 0;
        while heap.peek().unwrap().next_house <= house_number {
            let mut item = heap.pop().unwrap();
            assert_eq!(item.next_house, house_number);
            sum_of_elf_numbers += item.elf_number;
            item.next_house += item.elf_number;
            item.deliveries_to_do -= 1;
            if item.deliveries_to_do != 0 {
                heap.push(item);
            }
        }

        // stop when the input number is reached
        if (sum_of_elf_numbers * deliveries_per_house) >= INPUT {
            return house_number;
        }
        house_number += 1;
    }
}

fn main() {
    // part 1: infinite deliveries per elf, and 10 presents per house
    println!("{}", solver(u64::MAX, 10));
    // part 2: 50 deliveries per elf, and 11 presents per house
    println!("{}", solver(50, 11));
}

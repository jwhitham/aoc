
const INPUT: u64 = 34000000;


use std::collections::BinaryHeap;
use std::cmp::Ordering;


#[derive(Eq, PartialEq)]
struct HeapItem {
    elf_number: u64,
    next_house: u64,
}

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


fn main() {
    let mut heap: BinaryHeap<HeapItem> = BinaryHeap::new();
    let mut house_number = 1;

    loop {
        heap.push(HeapItem {
            elf_number: house_number,
            next_house: house_number,
        });

        let mut presents_div_10: u64 = 0;
        while heap.peek().unwrap().next_house <= house_number {
            let mut item = heap.pop().unwrap();
            assert_eq!(item.next_house, house_number);
            presents_div_10 += item.elf_number;
            item.next_house += item.elf_number;
            heap.push(item);
        }
        if (presents_div_10 * 10) >= INPUT {
            println!("{} {}", house_number, presents_div_10 * 10);
            break;
        }
        house_number += 1;
    }
}

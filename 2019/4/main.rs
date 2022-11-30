
const START: &str = "145852";
const END: &str = "616942";

fn advance(password: &mut Vec<u8>, start: usize) {
    for clear in start + 1 .. password.len() {
        password[clear] = b'0';
    }
    let mut index = start;
    loop {
        password[index] += 1;
        if password[index] <= b'9' {
            break; // no carry
        }
        password[index] = b'0';
        if index == 0 {
            break; // overflow
        }
        index -= 1;
    }
}



// Two adjacent digits are the same (like 22 in 122345).
fn first_invalid_by_rule_3(password: &Vec<u8>, part2: bool) -> usize {
    for index in 1 .. password.len() {
        if password[index - 1] == password[index - 0] {
            // rule is met
            let mut ok = true;
            if part2 {
                // OR IS IT? only if this is not part of a larger sequence
                let before_ok = (index <= 1) || (password[index - 2] != password[index - 1]);
                let after_ok = (index >= password.len() - 1)
                        || (password[index + 0] != password[index + 1]);
                ok = before_ok && after_ok;
            }
            if ok {
                return password.len();
            }
        }
    }
    // at least the last character is wrong
    return password.len() - 1;
}

// Going from left to right, the digits never decrease; they only ever increase
// or stay the same (like 111123 or 135679).
fn first_invalid_by_rule_4(password: &Vec<u8>) -> usize {
    for index in 1 .. password.len() {
        if password[index - 1] > password[index - 0] {
            return index;
        }
    }
    // rule is met
    return password.len();
}

// search for the next password and count validity
fn count_valid_in_range(start: &str, end: &str, part2: bool) -> usize {
    let mut password: Vec<u8> = Vec::from(start.as_bytes());
    let end_as_vec: Vec<u8> = Vec::from(end.as_bytes());
    let final_index = password.len() - 1;
    let mut count_valid: usize = 0;

    while password <= end_as_vec {
        // move past anything invalid
        let invalid3 = first_invalid_by_rule_3(&password, part2);
        let invalid4 = first_invalid_by_rule_4(&password);
        let invalid = usize::min(invalid3, invalid4);
        if invalid > final_index {
            // valid
            count_valid += 1;
            advance(&mut password, final_index);
        } else {
            // not valid
            advance(&mut password, invalid);
        }
    }
    return count_valid;
}

#[test]
fn test_part_2() {
    let mut password: Vec<u8> = Vec::from("112233".as_bytes());
    assert_eq!(first_invalid_by_rule_3(&password, true), password.len());
    password = Vec::from("123444".as_bytes());
    assert_eq!(first_invalid_by_rule_3(&password, true), password.len() - 1);
    password = Vec::from("111122".as_bytes());
    assert_eq!(first_invalid_by_rule_3(&password, true), password.len());
}

fn main() {
    println!("{}", count_valid_in_range(START, END, false));
    println!("{}", count_valid_in_range(START, END, true));
}


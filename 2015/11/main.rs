

fn advance(password: &mut Vec<u8>, start: usize) {
    for clear in start + 1 .. password.len() {
        password[clear] = b'a';
    }
    let mut index = start;
    loop {
        password[index] += 1;
        if password[index] <= b'z' {
            break; // no carry
        }
        password[index] = b'a';
        if index == 0 {
            break; // overflow
        }
        index -= 1;
    }
}



// Passwords must include one increasing straight of at least three
// letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip
// letters; abd doesn't count.
fn first_invalid_by_rule_1(password: &Vec<u8>) -> usize {
    for index in 2 .. password.len() {
        if (password[index - 2] + 1) == password[index - 1]
        && (password[index - 1] + 1) == password[index - 0] {
            // rule is met
            return password.len();
        }
    }
    if (password[password.len() - 3] + 1) == password[password.len() - 2] {
        // at least the last character is wrong
        return password.len() - 1;
    } else {
        // at least the last two characters are wrong
        return password.len() - 2;
    }
}
// Passwords may not contain the letters i, o, or l, as these letters
// can be mistaken for other characters and are therefore confusing.
fn first_invalid_by_rule_2(password: &Vec<u8>) -> usize {
    for index in 0 .. password.len() {
        if password[index] == b'i'
                || password[index] == b'o'
                || password[index] == b'u' {
            return index;
        }
    }
    // rule is met
    return password.len();
}
// Passwords must contain at least two different, non-overlapping pairs
// of letters, like aa, bb, or zz.
fn first_invalid_by_rule_3(password: &Vec<u8>) -> usize {
    let invalid_index = password.len();
    let mut pair1_index: usize = invalid_index;
    let mut pair2_index: usize = invalid_index;
    for index in 1 .. password.len() {
        if password[index - 1] == password[index] {
            // pair found
            if pair1_index == invalid_index {
                pair1_index = index;
            } else if pair2_index == invalid_index
            && password[pair1_index] != password[index] {
                pair2_index = index;
            }
        }
    }
    if pair1_index == invalid_index {
        // no pairs at all - final three characters must change
        return password.len() - 3;
    } else if pair2_index == invalid_index {
        // one pair
        if password[password.len() - 2] == password[pair1_index] {
            // final two characters must change
            return password.len() - 2;
        } else {
            // final character must change
            return password.len() - 1;
        }
    } else {
        // two pairs - ok
        return password.len();
    }
}

// search for the next password
fn find_next_password(input_str: String) -> String {
    let mut password: Vec<u8> = Vec::from(input_str.as_bytes());
    let final_index = password.len() - 1;

    // always move to the next password
    advance(&mut password, final_index);

    loop {
        // move past anything invalid
        let invalid1 = first_invalid_by_rule_1(&password);
        let invalid2 = first_invalid_by_rule_2(&password);
        let invalid3 = first_invalid_by_rule_3(&password);
        let mut invalid = invalid1;
        if invalid > invalid2 {
            invalid = invalid2;
        }
        if invalid > invalid3 {
            invalid = invalid3;
        }
        if invalid > final_index {
            break; // valid
        }
        advance(&mut password, invalid);
    }
    return std::str::from_utf8(password.as_slice()).unwrap().to_string();
}


fn test() {
    assert_eq!(find_next_password("abcdefgh".to_string()), "abcdffaa");
    assert_eq!(find_next_password("ghijklmn".to_string()), "ghjaabcc");
}

fn main() {
    test();    
    let input = "vzbxkghb".to_string();
    let first = find_next_password(input);
    println!("{}", first);
    let second = find_next_password(first);
    println!("{}", second);
}


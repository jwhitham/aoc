


fn find_next(input_str: String) -> String {
    let mut input_bytes: Vec<u8> = Vec::from(input_str.as_bytes());
    let mut index = input_bytes.len();
    while index > 0 {
        index -= 1;
        input_bytes[index] += 1;
        if input_bytes[index] < b'z' {
            break;
        }
        input_bytes[index] = b'a';
    }
    return std::str::from_utf8(input_bytes.as_slice()).unwrap().to_string();
}


fn main() {
    let input = "vzbxkghb".to_string();
    let first = find_next(input);
    println!("{}", first);
    let second = find_next(first);
    println!("{}", second);
}


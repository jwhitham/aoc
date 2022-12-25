
use std::fs::File;
use std::io::{self, BufRead};


type Word = i64;

fn parse_snafu(text: &str) -> Word {
    let mut total: Word = 0;
    for b in text.bytes() {
        total *= 5;
        match b {
            b'2' => { total += 2; },
            b'1' => { total += 1; },
            b'0' => { total += 0; },
            b'-' => { total -= 1; },
            b'=' => { total -= 2; },
            _    => {},
        }
    }
    return total;
}

fn unparse_snafu(val: Word) -> String {
    let mut text = String::new();
    let mut total = val;
    loop {
        let r = total % 5;
        match r {
            2 | -3 => { text.insert(0, '2'); },
            1 | -4 => { text.insert(0, '1'); },
            4 | -1 => { text.insert(0, '-'); },
            3 | -2 => { text.insert(0, '='); },
            _      => { text.insert(0, '0'); },
        }
        match r {
            -3 => { total -= 5; }
            -4 => { total -= 5; }
            4 =>  { total += 5; }
            3 =>  { total += 5; }
            _ =>  {},
        }
        total /= 5;
        if total == 0 {
            break;
        }
    }
    return text;
}

fn load(filename: &str) -> Word {
    let file = File::open(filename).unwrap();
    let mut total: Word = 0;
    for line in io::BufReader::new(file).lines() {
        if let Ok(line_string) = line {
            total += parse_snafu(line_string.as_str());
        }
    }
    return total;
}


#[test]
fn test_part1() {
    assert_eq!(parse_snafu("1-0---0"), 12345);
    assert_eq!(parse_snafu("1121-1110-1=0"), 314159265);
    assert_eq!(load(&"test"), 4890);

    fn loop_test(t: &str) {
        let x = parse_snafu(t);
        let y = unparse_snafu(x);
        println!("loop: input {} decimal {} output {}", t, x, y);
        assert_eq!(y, t);
    }
    loop_test("0");
    loop_test("1");
    loop_test("2");
    loop_test("-");
    loop_test("=");
    loop_test("22");
    loop_test("20");
    loop_test("-2");
    loop_test("--");

    assert_eq!(unparse_snafu(12345), "1-0---0".to_string());
    assert_eq!(unparse_snafu(4890), "2=-1=0".to_string());
    assert_eq!(unparse_snafu(314159265), "1121-1110-1=0".to_string());
}

fn main() {
    println!("{}", unparse_snafu(load(&"input")));
}


use std::fs::File;
use std::io::{self, BufRead};

// input:
// To continue, please consult the code grid in the manual.  
// Enter the code at row 2947, column 3029.
//

const ROW: u64 = 2947;
const COLUMN: u64 = 3029;

const FIRST_CODE: u64 = 20151125;
const MULTIPLY_BY: u64 = 252533;
const MODULO_BY: u64 = 33554393;


fn row_column_to_linear(row: u64, col: u64) -> u64 {
    // First compute the number on the first row just before the diagonal containing (row, col)
    // Note: triangle number T(n) = (n * (n + 1)) / 2
    let sum = row + col - 1;
    let triangle_number = (sum * (sum - 1)) / 2;

    // add the column number to get the correct number
    return triangle_number + col;
}

fn compute_value(linear: u64) -> u64 {
    let mut value = FIRST_CODE;
    for i in 1 .. linear {
        value = (value * MULTIPLY_BY) % MODULO_BY;
    }
    return value;
}

#[test]
fn test_rcl() {
    assert_eq!(row_column_to_linear(1, 1), 1);
    assert_eq!(row_column_to_linear(2, 1), 2);
    assert_eq!(row_column_to_linear(1, 2), 3);
    assert_eq!(row_column_to_linear(3, 1), 4);
    assert_eq!(row_column_to_linear(2, 2), 5);
    assert_eq!(row_column_to_linear(1, 3), 6);
    assert_eq!(row_column_to_linear(4, 2), 12);
    assert_eq!(row_column_to_linear(1, 5), 15);
}

#[test]
fn test_linear() {
    assert_eq!(compute_value(1), FIRST_CODE);
    assert_eq!(compute_value(2), 31916031);
    assert_eq!(compute_value(3), 18749137);
}

fn main() {
    println!("{}", compute_value(row_column_to_linear(ROW, COLUMN)));
}


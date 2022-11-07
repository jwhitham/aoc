
use std::fs::File;
use std::io::{self, BufRead};

const SIZE: usize = 102;
type BoardType = [[bool; SIZE]; SIZE];

fn advance(board_in: &BoardType, board_out: &mut BoardType) {
    for y1 in 1 .. SIZE - 1 {
        for x1 in 1 .. SIZE - 1 {
            // count neighbours
            let mut count = 0;
            if board_in[y1 - 1][x1 - 1] { count += 1; }
            if board_in[y1 + 0][x1 - 1] { count += 1; }
            if board_in[y1 + 1][x1 - 1] { count += 1; }
            if board_in[y1 - 1][x1 + 0] { count += 1; }
            if board_in[y1 + 1][x1 + 0] { count += 1; }
            if board_in[y1 - 1][x1 + 1] { count += 1; }
            if board_in[y1 + 0][x1 + 1] { count += 1; }
            if board_in[y1 + 1][x1 + 1] { count += 1; }
            // current state of light
            if board_in[y1][x1] {
                board_out[y1][x1] = (count == 2) || (count == 3);
            } else {
                board_out[y1][x1] = count == 3;
            }
        }
    }
}

fn get_input() -> BoardType {
    // Read input (initial state of the board)
    let file = File::open("input").unwrap();
    let lines = io::BufReader::new(file).lines();
    let mut board1: BoardType = [[false; SIZE]; SIZE];
    let mut y = 0;
    for line in lines {
        if let Ok(line_string) = line {
            let mut x = 0;
            for col in line_string.chars() {
                if col == '#' {
                    board1[y + 1][x + 1] = true;
                }
                x += 1;
                if x >= (SIZE - 2) {
                    break;
                }
            }
        }
        y += 1;
        if y >= (SIZE - 2) {
            break;
        }
    }
    return board1;
}

fn count_on(board1: &BoardType) -> usize {
    let mut count = 0;
    for y in 0 .. SIZE {
        for x in 0 .. SIZE {
            if board1[y][x] {
                count += 1;
            }
        }
    }
    return count;
}

fn light_corners(board: &mut BoardType) {
    board[1][1] = true;
    board[SIZE - 2][1] = true;
    board[SIZE - 2][SIZE - 2] = true;
    board[1][SIZE - 2] = true;
}


fn main() {
    // Part 1
    let mut board1 = get_input();
    let mut board2: BoardType = [[false; SIZE]; SIZE];
    for _ in 0 .. 50 {
        advance(&board1, &mut board2);
        advance(&board2, &mut board1);
    }
    println!("{}", count_on(&board1));

    // Part 2
    board1 = get_input();
    light_corners(&mut board1);
    for _ in 0 .. 50 {
        advance(&board1, &mut board2);
        light_corners(&mut board2);
        advance(&board2, &mut board1);
        light_corners(&mut board1);
    }
    println!("{}", count_on(&board1));
}

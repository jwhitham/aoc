
use std::fs::File;
use std::io::{self, BufRead};


const WIDTH: usize = 25;
const HEIGHT: usize = 6;

struct Layer {
    pixel: [[u8; WIDTH]; HEIGHT],
}

fn load() -> Vec<Layer> {
    let file = File::open("input").unwrap();
    let line = io::BufReader::new(file).lines().next().expect("line").unwrap();
    let bytes = line.as_bytes();

    assert_eq!(bytes.len() % (WIDTH * HEIGHT), 0);
    let num_layers = bytes.len() / (WIDTH * HEIGHT);

    let mut layers: Vec<Layer> = Vec::new();
    let mut index: usize = 0;
    for _ in 0 .. num_layers {
        let mut layer = Layer {
            pixel: [[0; WIDTH]; HEIGHT],
        };
        for y in 0 .. HEIGHT {
            for x in 0 .. WIDTH {
                layer.pixel[y][x] = bytes[index];
                index += 1;
            }
        }
        layers.push(layer);
    }
    assert_eq!(index, bytes.len());
    return layers;
}

fn part1() {
    let layers = load();
    let mut result: usize = 0;
    let mut least_zeroes: usize = usize::MAX;

    for layer in layers {
        let mut zeroes: usize = 0;
        let mut ones: usize = 0;
        let mut twos: usize = 0;
        for y in 0 .. HEIGHT {
            for x in 0 .. WIDTH {
                match layer.pixel[y][x] {
                    b'0' => zeroes += 1,
                    b'1' => ones += 1,
                    b'2' => twos += 1,
                    _ => {},
                }
            }
        }
        if zeroes < least_zeroes {
            least_zeroes = zeroes;
            result = ones * twos;
        }
    }
    println!("{}", result);
}

fn part2() {
    let mut layers = load();
    let mut combined = Layer {
        pixel: [[0; WIDTH]; HEIGHT],
    };
    layers.reverse();

    for layer in layers {
        for y in 0 .. HEIGHT {
            for x in 0 .. WIDTH {
                match layer.pixel[y][x] {
                    b'0' | b'1' => combined.pixel[y][x] = layer.pixel[y][x],
                    _ => {},
                }
            }
        }
    }
    for y in 0 .. HEIGHT {
        for x in 0 .. WIDTH {
            print!("{}", match combined.pixel[y][x] {
                b'1' => '#',
                _ => ' ',
            });
        }
        println!();
    }
}

fn main() {
    part1();
    part2();
}


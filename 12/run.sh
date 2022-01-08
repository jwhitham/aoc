#!/bin/bash -xe
gfortran -o part1 part1.f
gfortran -o part2 part2.f
./part1 < input
./part2 < input

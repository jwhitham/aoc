#!/bin/bash -xe
/f/GNAT/2017/bin/gcc -o part1.exe -m32 part1.S -g && cat input | ./part1.exe

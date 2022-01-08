#!/bin/bash -xe
/f/GNAT/2017/bin/gcc -o part2.exe -m32 part2.S -g && cat input | ./part2.exe

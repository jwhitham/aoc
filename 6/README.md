
# Day 6 - VHDL

[Link to problem](https://adventofcode.com/2020/day/6)

It seemed like this exercise would map well to hardware. In particular,
each group is represented by 26 bits, and then you have to count
how many of these bits are '1'. VHDL describes logic circuits but
also test benches - and the test benches are effectively just
ordinary programs that can read and write input files as well as driving
the logic signals of the "hardware". 

In this solution the test bench reads the input file and generates signals
to describe each line of the file. The "hardware" components manage the
26 bits representing the group, apply union/intersection operations and
do the "population count".

It was nice to write some VHDL again. It has been a while since I worked
on FPGAs and dealt with it every day. It is a pleasant language to use
and the ability to define parameterisable generic components was useful even
in this tiny exercise.



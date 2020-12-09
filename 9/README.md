
# Day 9 - BBC BASIC

[Link to problem](https://adventofcode.com/2020/day/9)

For this one I thought I'd return to a language which I have not used
since around 1990. BBC BASIC came with the BBC Micro: I also used a
PC port which [still exists](https://www.bbcbasic.co.uk/bbcbasic.html)
and has since been updated for Windows. 1980s microcomputers almost
invariably came with some kind of BASIC in the boot ROM, and BBC BASIC
was regarded as one of the better ones. For instance you can have named
functions and procedures, and it is possible to avoid GOTO completely. I
picked up the DOS version of BBC BASIC again and tried to remember
how to use it.

The language has some features which I think are intended to encourage
better structure: for instance, you cannot "break" out of a loop,
or return early within a procedure. That's understandable, and
helps to avoid BASIC programs becoming a rats nest of GOTOs and GOSUBs,
but it combines badly with the limitation of "IF" statements, which is
that the body must appear on the same line as "IF". This makes it very
difficult to write conditional code with a readable structure. I made
the "IF" statements call procedures where possible.

My heart sank when I found that the full "puzzle input" contained
numbers that couldn't be represented as 32 bit integers, but after
I'd written an adder for integers represented as BCD strings,
I found that the 32-bit limitation didn't matter anyway as the puzzle
solver never reached those values.

The solution for part 1 uses a ring buffer for both the input
values and the pairs calculated from them, avoiding some recalculation.


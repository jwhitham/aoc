
# Day 11 - IBM 1401 assembly code

[Link to problem](https://adventofcode.com/2020/day/11)

[The IBM 1401](http://ibm-1401.info/) was the first mass-produced 
computer. It does not use integrated circuits, 8-bit bytes or ASCII,
and it has no hardware stack and no "call" or "return" instructions.
It was a (relatively) low-cost computerised version of IBM's punched
card machines. The CPU uses decimal numbers for everything, even
addressing. Programs are usually stored on punched cards, though
they may also be stored on tape: the vacuum-column 729 tape drives are
the ones that appear as "the computer" in old films.
[1401s can be seen in various museums](http://ibm-1401.info/WorldInventoryIBM1401.html),
[https://www.youtube.com/watch?v=uFQ3sajIdaM](some restored and working).

I
[read that it is hard to write programs for the IBM 1401](https://www.curiousmarc.com/computing/ibm-1401-mainframe/ibm-1401-programming)
and so I had to find out for myself. I used 
[the ROPE environment](https://github.com/jpf/ROPE/commit/5a6aa381c19bf49cf61d44d93862db593e994a07)
which includes Van Snyder's Autocoder (assembler) and a 1401 simulator.

Memory was a big limitation. The problem requires 95x98 characters
to store the state. This will fit in the 1401's memory, which
allows up to 16000 characters of RAM, but it is awkward to do
address calculations on any address above 999 because all addresses
consist of three decimal digits plus some "zone bits". The original
machine also had no method of index addressing, so you cannot do
array subscripts or dereference a pointer without self-modifying code!
The index feature was awkwardly added to the architecture
later, but not all manuals describe it, and this
was a bit of a roadblock since the AOC problem is a cellular automaton
and there is a need to process an array of cells. Furthermore, I found
indexing didn't work well with addresses above 999.

I made a version of the program that worked on one line at a time and
stored other lines on tape. In this way the arrays could be kept in
the low memory area. For part 1, I stored three lines,
so adjacent cells are in RAM when each cell is processed. Part 1 
used a single north-south pass to process the array.

For part 2, I needed a north-south pass and a south-north pass to
compute the visibility count for each cell. The working tape runs
backwards during the south-north pass.

Implementation of part 2 was very complex
so I worked in three stages. First I made a Python model that
solved the problem by storing everything in RAM, then I made a second 
Python model that worked on one line at a time, and finally, I translated
this to 1401 code. The 1401 program
logged intermediate states to a debugging tape. Comparisons of this
debugging tape to data from the model helped me to find bugs
(usually off-by-one errors).

The final program uses four tapes which have to be assigned to disk
files using settings in ROPE (e.g. part2.mt1 is tape 2 for the part 1
program). The 1401's tape control is actually simple. It is hard
to imagine a modern computer where "print a line", "rewind the tape"
and "read a block from tape" are all single machine instructions!

I think it is possible to solve the
problem using a single tape - indeed, in principle, it can be solved in RAM -
but this solution was easier to build and test. It helps to keep one read-only
tape that's exclusively for input, and one write-only tape exclusively
for debugging. Otherwise you must regenerate the input tape before
running.

[This book](http://bitsavers.org/pdf/ibm/1401/Programming_the_1401_1962.pdf)
was the most detailed reference I found, but 
[this book](http://bitsavers.trailing-edge.com/pdf/ibm/1401/A_Guide_to_1401_Programming_1961.pdf) may be a better introduction,
though it does not mention index registers. I didn't find
anything like a 1401 architecture reference manual,
with detailed information on each instruction's encoding and behaviour,
but the relevant information can be found by searching these books.


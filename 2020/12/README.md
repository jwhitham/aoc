
# Day 12 - FORTRAN 77

[Link to problem](https://adventofcode.com/2020/day/12)

FORTRAN has nice facilities for processing formatted lines
from an input file, and so this was quite an easy one. The
program structure was straightforward and similar to what I
would write in most other languages. 

Perhaps the GNU FORTRAN compiler is more tolerant than others,
because I have found old FORTRAN programs to be quite hard to read:
[here, for example](https://github.com/osresearch/advent/blob/master/AMAIN.FOR).
They don't use indenting to show structure, and GOTO is frequently used.
It seems these are not required, though in old FORTRAN there is
a strict limit on the length of a line. In this program, the only odd
anachronism was the need to refer to line labels for
formatting and error handling, and more modern revisions of the
language do not have this limitation.


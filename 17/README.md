
# Day 17 - ALGOL 68

[Link to problem](https://adventofcode.com/2020/day/17)

I wanted to take the opportunity to try an old programming language,
no longer in general use. I was aiming for ALGOL 60, which was enormously
influential on subsequent programming languages, to the extent that
languages such as C and Pascal have been called
[ALGOL-like](https://en.wikipedia.org/wiki/ALGOL_60). But that will
have to wait for another day, because I was not able to find
a usable ALGOL 60 compiler or interpreter capable of running a
this program, though I tested three of them! It does not help that ALGOL 60
is so old that there is no exact standard for representing identifiers,
keywords and literals(!) and so a program made for ALGOL 60 environment
will not normally work with any other unless translated.

I had more luck with [ALGOL 68](https://en.wikipedia.org/wiki/ALGOL_68) thanks to
[Algol68Genie](https://jmvdveer.home.xs4all.nl/en.algol-68-genie.html)
which has some really excellent
[documentation](https://jmvdveer.home.xs4all.nl/learning-algol-68-genie.pdf)
and worked out of the box. So I used it!

In this case the problem is a many-dimensional cellular automaton
simulation. I reused some ideas from day 11 here. The algorithm is
about as simple as it could be: I was relieved not to be asked to
simulate thousands of cycles in part 2, because the method used is
so inefficient. However, keeping a margin avoids the need to treat
the edge as a special case. You can be sure that the required space
cannot grow beyond the number of iterations (six) so it is possible
to preallocate the space.

I found that ALGOL 68 is only slightly related to ALGOL 60. It is not just
a few extensions for the earlier language - it is effectively a complete
redesign. An annoying aspect of the language is that semicolons are
optional at the end of a block, but required everywhere else, which makes
it hard to rearrange lines when refactoring.

The language appears to have a powerful static type system which I barely
touched. ALGOL 60 does not have anything so complex. Both languages
allow inner procedures, working correctly if you access variables in
the outer procedure. You can declare variables within blocks.
Multidimensional arrays are no problem (fortunately) and the FOR loop
syntax in ALGOL 68 is pleasant. The language reminds me most of Ada, but
it is not as verbose: indeed, the verbosity seems to have been reduced
since ALGOL 60, with much more shorthand. However, the language itself
is clearly very complex, and I have barely touched it here.


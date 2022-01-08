
# Day 21 - Ruby

[Link to problem](https://adventofcode.com/2020/day/21)

The AOC organiser has again been kind: the input gives
only one possible route to the solution, there is no searching.

This time I used Ruby. Ruby is often compared to Python; I have
much more familiarity with Python and I think my Ruby code is
quite Pythonic as a result. In particular I find it hard to
resist writing "()" at the end of every function call, even though
this is not necessary in Ruby, and it is probably considered bad style.
Real Ruby programmers would write more compact code.

There is a Ruby pattern which is not at all Pythonic, and that is
the use of anonymous functions/closures for every item in a list or
set. Ruby makes this as easy as writing the body of a "for" loop,
and I used it a lot here. The string processing code is basically the
same as it would be in Python: the "split" function is heavily used
to turn a string into a list of fields. In Ruby you can modify strings
in place by calling "!" versions of the functions that act on them.

It is easy to imagine a world where Ruby, rather than Python, had
gained the market share. They both fill the Perl niche, but are
nicer to use, especially once you start using references and objects.
If I was using Ruby frequently, I think I would mainly miss the
static type checking support that's now in Python (i.e. mypy).


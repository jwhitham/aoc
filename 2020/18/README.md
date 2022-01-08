
# Day 18 - Python, Lex and Yacc

[Link to problem](https://adventofcode.com/2020/day/18)

Lex and Yacc are great tools for problems like this. The originals
generate C source code. They have been adapted for other languages.
I found a [Python version named "ply"](https://github.com/dabeaz/ply)
while looking at Algol interpreters, so I thought I would give it a try.

I think it should not be too hard to write a hand-made parser for
this particular problem. But it is better to use the right tool for
the job, and in this Pythonic form, Lex and Yacc are very suitable.


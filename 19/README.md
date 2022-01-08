
# Day 19 - C, Lex and Yacc

[Link to problem](https://adventofcode.com/2020/day/19)

It is another problem about parsing. In this case I am fairly
sure that the intention is that I should solve part 1 using
a deterministic finite automaton (DFA); and then, for part 2, the
DFA has to be extended with some recursive capability.

Part 1 can be quickly solved by converting the problem to a
regular expression which can be fed into one of the many regular
expression libraries. Part 2 can almost be solved in that way,
but not quite, because of the need to be sure that the number
of invocations of some rule X matches the number of invocations of
some rule Y. A quick solution is probably possible by extracting
the relevant part of the input string and then checking
it separately.

The hard way to solve the problem is effectively to build a
regular expression library yourself; make an NDFA from the
grammar, then turn it into a DFA, then use it for matching. This
does have the advantage that it should be possible to convert it
to add the extra rules for part 2 - it might be a "pushdown"
automaton - but it's definitely a high-effort solution.

I was still thinking about Lex and Yacc from yesterday so I
decided to use them again, but this time from C. The problem
description hints that you don't need such a powerful parser, but, well,
it's a reusable tool, so the extra power is free. The C solution
involves multiple code-generating steps.



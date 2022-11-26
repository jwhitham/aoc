# Day 19

[Link to problem](https://adventofcode.com/2015/day/19)

At first I thought, "Ah, it's the annual question on context-free grammars",
though I did also hope it might be going somewhere else, and part 1 did hint
at some other destination. Because of the difficulty of solving part 2, I did
attempt other methods, such as a greedy search, but without success.

In other years these problems were solvable with LR(1) parsers, and those exercises
were most easily completed by bringing in some appropriate "compiler compiler"
library or tool to generate the parser from the grammar. In Python you might use
[ply](https://github.com/dabeaz/ply), in C it would be something resembling
yacc, and as I'm currently learning about Rust, it would be
[lalrpop](https://github.com/lalrpop/lalrpop) or maybe Plex, though I found Plex
very hard to use. (Plex relies on wizard-level Rust features which still only appear
in nightly builds, and if anything is wrong, the error messages are very hard
to understand, whereas lalrpop is straightforward.)

In this case the problem is not solvable with a LR(1) parser because the
grammar is full of ambiguities which manifest as "shift/reduce conflicts"
when the parser is generated. "ply" will treat this error as a warning
and generate a parser anyway, which does work on some inputs (including mine)
and this generated an answer that is accepted by AOC (207), but it is a fundamentally
unsatisfying solution because (1) it does not work on all inputs, not
even the "HOHOHO" example, (2) I think there's no guarantee that this is truly
the minimal solution. For a real solution, a more powerful parser is needed, and we
step outside the undergraduate CS "comfort zone" into the wider world
of context-free languages (unfamiliar territory for me). From
[the usual starting point](https://en.wikipedia.org/wiki/Context-free_grammar)
I got into reading about [Earley parsers](https://en.wikipedia.org/wiki/Earley_parser)
and tried to apply this approach (it tracks all possible parser states
as the input string is parsed). This indicated that the input could be parsed,
and with the help of [somebody else's Earley
implementation](https://github.com/tomerfiliba/tau/blob/ebf92cd99f9abf1903927e1c91f9e37fcd522bc7/earley3.py)
I was able to get the same answer I'd got from "ply". This also worked for "HOHOHO",
though I am still unsatisfied because I can't be sure the solution is minimal
(though AOC accepts it). The tree of all possible solutions seems to be massive and
I was only able to get an answer by accepting the first one.

Eventually I decided to give up and look at other people's answers. It seems
that some people were given easier variants of the problem.

* [vstrimaitis](https://github.com/vstrimaitis/aoc-2015/blob/master/day_19.py) got
  input data that could be solved by greedily applying grammar rules until no more
  can be applied - at which point, either the problem is solved, or the program
  randomises the priority of the rules and starts again. This does not work for me.

* [ape](https://github.com/Ape/aoc_2015_day19/blob/master/part2.py) got
  input data that could be solved by A\* search. The size of the molecule gives
  a useful heuristic to guide the search, and at each search step, all possible rules
  are attempted. This seems a reasonable approach to me, but it's not tractable
  for my input data.

* [Edd Mann](https://eddmann.com/posts/advent-of-code-2015-day-19-medicine-for-rudolph/)
  has input data where "The input has been constructed in such a way that there
  is no possibility for ambiguity, with only one path back to e".

[Various others](https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/)
were given a mixture of inputs that were either easy or hard. Easy ones were solvable
by making the largest substitution possible at each step,
whereas hard ones needed a powerful parser for general context-free grammars,
with CYK being one other suggestion.

Arguably the most elegant solution is based on pure reasoning about the symbols
which appear in the rules, followed by counting the number of times specific symbols
appear in the molecule, but this is rather unsatisfying to me, since this sort of
solution is specific to the grammar rules rather than the molecule. (The rules seem to be
the same in all input.)

The difficulty of the input data was plainly quite variable. I think this variation was
probably not intended. Perhaps the greedy approaches were always supposed to work. 


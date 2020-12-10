
# Day 10 - Haskell

[Link to problem](https://adventofcode.com/2020/day/10)

I'm very much a beginner with Haskell and I am sure that
an experienced user would come up with a much more compact
solution. I regret not doing the Haskell course while at University
and though I did look on some occasions since then, I never got very far.
I think that my Haskell code is not at all idiomatic and is
very Lisp-like with heaps of unnecessary brackets. 

In this exercise, writing the first part went well, but the second
part was hard to write efficiently. My initial attempts to solve it
would produce the correct answer but didn't scale to the problem size.

```
reachable (a : b : c : d : rest) =
        ((if (can_reach a b) then (reachable (b : c : d : rest)) else 0) +
         (if (can_reach a c) then (reachable (c : d : rest)) else 0) +
         (if (can_reach a d) then (reachable (d : rest)) else 0))
```

I had the mistaken idea that Haskell would "notice" that the
same list was being passed to the same function many times, and
would remember the result. Perhaps this may happen in other
circumstances... being a beginner, I do not know.
I decided instead to turn the input list into an
intermediate list of (number\_of\_ways, value) pairs, which was effective.

I am also unhappy that my solution is not parameterised for the
maximum value "3". My definition of ways\_to\_reach will only look ahead
up to 3 list items. A better solution would allow this to be set.



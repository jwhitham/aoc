
# Day 22 - F#

[Link to problem](https://adventofcode.com/2020/day/22)

Great problem today - particularly part 2. There was a
subtlety in the specification which I initially misunderstood,
namely that the subgame is not played with the entire deck,
but rather with the top N cards, where N is the value of the
card drawn. Running the example input produced the same result
despite this misunderstanding, but the full problem had a long
running time (perhaps not infinite but certainly intractable).

I had not used F# before and I think I am generally quite
weak on functional languages, so I don't know if I got a good
solution. It is tail recursive (unless entering a subgame) and
may be relatively good. I am unsure of the cost of the set membership
tests which are needed to detect if the game is repeating itself. It
seems that, in a functional language, adding an item to a set must
always involve making a copy of the set, so the underlying set
representation must be able to handle that efficiently.

In F# I found that some Haskell knowledge was transferable. One sticking point was
figuring out how to declare the types of parameters and returns - this is
not initially required because the types can usually be inferred, but if
you mess up any of the syntax, then the inference may not work. In this,
case, being able to explicitly declare the types is really helpful in
tracking down the actual error.

F# syntax seems a bit awkward in that function calls sometimes look
like Haskell, e.g. '(get_result 1 2)', and sometimes like C#,
e.g. 'list.GetSlice(1, 2)'. I found this confusing, but I am only
a beginner.



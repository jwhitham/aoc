
# Day 14 - Typescript

[Link to problem](https://adventofcode.com/2020/day/14)

I wrote a very naive solution to part 2 and was surprised that it completed
in a reasonable time. The AOC organiser has been very kind by putting
at most nine "X" bits in the word. If a larger number of "X" bits were
present, then this solution would be unusable, requiring too much time
and memory.

I used Typescript here because I like it. You can't get away from Javascript
nowadays, but in Typescript you are almost insulated from the idiosyncracies
of Javascript, and things work sensibly. Two exceptions are that you
have to use Javascript's numerical type, which is a float or an int
depending on the value. And, when Javascript code calls back into Typescript, it
will mess up the "this" pointer unless you are cautious. I think these issues
must be difficult to fix. In general, Typescript does a great job of hiding
the bad design of Javascript.

## Update

I was bothered by the bad solution to part 2, being sure there was a better
solution. In particular I do not like how the example input, i.e.

```
    mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    mem[8] = 11
    mem[7] = 101
    mem[8] = 0
```

would cause my part 2 implementation to consume a huge amount of CPU and RAM.
What I have now (as "part 2A") is a representation based on a tree
in which the root represents the leftmost bit, leaves represent values in
memory, and nodes may have one child (representing 'X') or 2 children
representing '0' and '1'. An 'X' node may be split into two subtrees
if a new input means that the bit is important; subtrees may also be
combined if they are equivalent. I think this is a more satisfactory design.


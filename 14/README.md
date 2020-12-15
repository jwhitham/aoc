
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
must be difficult to fix, because generally, Typescript does a great job
in hiding such nonsense.


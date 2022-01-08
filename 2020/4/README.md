
# Day 4 - Bash

[Link to problem](https://adventofcode.com/2020/day/4)

This solution makes heavy use of "egrep". This turned out to be
a good thing in part 2.

I learned that Bash scripts like this are very slow,
especially on Windows. In fact, it was so slow that the
same script running on a Raspberry Pi 2 easily beat my desktop PC,
completing in a fraction of the time. I think this is because of
the overhead of starting processes on Windows, which is substantial. 


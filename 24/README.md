
# Day 24 - Lua

[Link to problem](https://adventofcode.com/2020/day/24)

This turned out to be another cellular automata puzzle, but with hex tiles.
I represented the hex tiles using the approximate coordinates of their centre
points, so moving southeast means moving east by 1 unit and south by 2 units.

The space was potentially infinite. I think that using a hash table is a good
way to represent this (better than an array) because it is a naturally sparse
data structure which can expand as required. Lua has a "table" type which also
acts as an array: unfortunately I could not use a two-dimensional hash key (y,x)


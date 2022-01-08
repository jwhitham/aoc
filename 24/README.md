
# Day 24 - Lua

[Link to problem](https://adventofcode.com/2020/day/24)

This turned out to be another cellular automata puzzle, but with hex tiles.
I represented the hex tiles using the approximate coordinates of their centre
points, so moving southeast means moving east by 1 unit and south by 2 units.

The space was potentially infinite. I think that using a hash table is a good
way to represent this because it is a naturally sparse
data structure which can expand as required. In Lua there is no difference between
a hash table and an array: both are "tables", which is convenient.
Unfortunately I could not use a two-dimensional hash key (i.e. y, x)
so I instead used a table containing tables. Part 2 temporarily
places values into the table to indicate how many black hex tiles are adjacent to
each tile.

Lua worked reasonably here. It is quite minimal in terms of the features provided,
which can be a very good thing. It reminds me a little of Javascript, but I
think Lua has better syntax and better design.


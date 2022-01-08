
# Day 25 - Ada

[Link to problem](https://adventofcode.com/2020/day/25)

Not for the first time, Ada saved me from making a silly mistake. The
multiplication can easily result in a number larger than 2^32. In most
programming languages, if you used a 32-bit type, such a multiplication
would just overflow silently, keeping only the least significant 32 bits.
This is what happens in C, and in every language which has copied C's
semantics, which is almost all of them. But not in Ada, where an exception
is raised. This prompted me to use a 64-bit integer type instead.


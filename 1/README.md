
# Day 1 - Perl 5

[Link to problem](https://adventofcode.com/2020/day/1)

I tried to write an efficient solution by using a hash (dictionary)
as a quick way to check each possible solution.

In part 1, this worked nicely, and the program has linear time complexity.

In part 2, I sorted the array in order to make the search space smaller.

I learned that, by default, Perl's sort function will compare
integer array elements as if they were strings, which led to the
integers appearing in the wrong order (e.g. 100 before 2). This
problem is avoided by specifying the comparison function.

For part 2 I do not know the time complexity. It cannot be
worse than O(n^2), but it might be much better than that
because the search space is pruned.



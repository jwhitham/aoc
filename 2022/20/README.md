# Day 20 

[Link to problem](https://adventofcode.com/2022/day/20)

This problem seems to call for a double-ended queue or a linked list,
as the main operation is removing an element in one place and then
inserting it at another. However, that's not the whole problem,
as it's also necessary to process the elements in a specific order,
and this requires repeated searches for a specific element. If a deque or
linked list is used, each search will be O(N).

There's no need for anything smarter in this case, because the list size
is only 5000 elements. My first implementation worked with Vec, after
some minor struggles with off-by-one errors, fixed by comparing with the
examples (commit e8d1d5ee6cf68a51587e24b9ffedfb05a432ac54e).
Later I tried VecDeque, which I thought would be better, but was actually
slightly slower when benchmarked
(commit 62c1967ae6b7c2b84df87894043f9a5565ba12f7).

Is it possible to do better?

A hash table is not helpful for finding the element because its position
changes every time elements are added/removed. Updating the hash table
with new positions would also be O(N).

[2020 day 23](../../2020/23) seemed to involve a similar
problem, though there was a shortcut in that case. The solution is to
store the list in the form of a balanced binary tree - the leftmost leaf
in the tree is list element zero. The tree does not use a comparison function
to determine where elements should be placed - instead, it uses the list index.
The index for each tree node can be determined by counting the number of elements
to its left. This count is called the "rank" and it can be determined in
O(log N) operations.

This representation allows insertion and removal of list elements in O(log N) time,
regardless of the index, but the really useful feature is you can discover the
current index of any element. You need only store a pointer to each node, so if you
need to move the elements in a particular order, the pointers can appear in an ordered
list.

I made a C# class for this purpose in 2020 and I ported it to Rust for this problem,
as a crate named "[tree list](tree_list)".

The original class made heavy use of pointers (well, references, since C# is managed code).
An exact Rust port would require pointers with reference counting. I did attempt this,
but I found that I'm still not comfortable with Rust's pointer restrictions and it
is extremely hard to get any code to a state that the compiler will accept. Therefore
I assigned each tree node a unique reference number to be used in place of a pointer.
This is slower but leads to relatively readable code which works. The ownership issues
created by directly using pointers are side-stepped.

Theoretically the "tree list" should be faster than Vec or VecDeque, given enough
list elements, but for the actual problem size (5000) it appears to be about 50% slower
in benchmarks. This might be related to the use of references rather than pointers, or some
other issue. For example, being a binary tree, the cache behaviour is unlikely to be as good as Vec.




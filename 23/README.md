
# Day 23 - C#

[Link to problem](https://adventofcode.com/2020/day/23)

In C#, I was glad to be able to use an array of records - this
is an efficient way to represent the problem. Some managed
languages would force me to use an array of references to records,
because arrays can only contain primitive types. The extra
level of indirection would waste time and memory.

I went down a rabbit hole with part 2 and wasted a lot of time
trying to implement a list-like data structure which would allow
fast insertion/removal of an element at any index. This is possible.
Binary trees are normally used as ordered maps, relating a key to
a value, and that is how they appear in standard libraries. But
you can also use them to represent indexed data, with the nice property
that adding/removing elements can implicitly update the indexes of
later elements.

I mistakenly believed that knowing the
index of each element would be necessary to solve the problem and
proceeded to try to implement a balanced binary tree with the
required properties. This proved challenging in various ways.
Textbook and online descriptions of red/black or AVL tree operations
tend to be incomplete and/or confusing. For instance, they may be
incomplete because they describe only insertion and then regard deletion
as a mostly trivial variation (Knuth does this; trivial for Knuth is
not trivial for me.). They can be confusing because
of the difficulty of describing nodes during a "rotation" in which
parents swap with children. Sample code can be even more confusing,
with little explanation of what's happening. Unfortunately it's
necessary to understand exactly what's happening in order to adapt
the usual key-value purpose of the data structure to be indexed
instead. Despite some hours of work I was unable to
write a delete operation that didn't also unbalance the tree.

Then, during time away from the problem, I realised that it was
quite unnecessary to know the index at all, and that a doubly
linked list would be much better, with O(1) insert/delete operations
rather than O(log N). An array is used for finding a value in
O(1) time. Taking a break can be useful!



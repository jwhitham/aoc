
# Day 23 - C#

[Link to problem](https://adventofcode.com/2020/day/23)

In C#, I was glad to be able to use an array of records - this
is an efficient way to represent the problem. Some managed
languages would force an array of references to records,
because arrays can only contain primitive types. The extra
level of indirection would waste time and memory.

However, I went down a rabbit hole with part 2 and wasted a lot of time
trying to implement a list-like data structure which would allow
fast insertion/removal of an element at any index. 

During time away from the problem, I realised that it was
quite unnecessary to know the index at all, and that a doubly
linked list would be much better, with O(1) insert/delete operations
rather than O(log N). An array is used for finding a value in
O(1) time. Taking a break can be useful!


## Digression

Binary trees are normally used as ordered maps, relating a key to
a value, and that is how they appear in standard libraries. But
you can also use them to represent indexed data, with the nice
property that you can insert/access/remove elements by index, at
any position, in O(log N) time. This usage is described in textbooks
such as Knuth's TAOCP.

If the values in the list are also unique, you can use a hash table
or array to relate a value to its node within the binary tree, and
from the node, you can find the index in O(log N) time by iterating
towards the root.

I mistakenly believed that knowing the
index of each element would be necessary to solve the problem and
proceeded to try to implement a balanced binary tree with the
required properties. I thought this wouldn't be so difficult, because
I had studied balanced trees as part of my CS degree, but it is not
easy to get the details right.

Textbook and online descriptions of red/black or AVL tree operations
tend to be incomplete and/or confusing.

For instance, they may be incomplete because they describe only
insertion and then regard deletion as a mostly trivial variation
requiring minimal extra description. However, it is not so simple,
there are many subtle details. For example, I missed a small but important
detail in Knuth's textbook and ended up writing a broken delete
operation which would unbalance the tree. It took a while to debug this.

Descriptions may also be confusing because of the difficulty of describing
nodes during a "rotation" in which parents swap with children. You cannot
use terms like "parent" or "right child" because these relationships shift
around. But other names, e.g. "node p", "node q", are opaque. For this
reason, sample code is also confusing.

Sample code is also very diverse, even for the same data structure,
so you cannot typically combine a clear part of one sample with a clear
part of another. For instance an implementation may use
numbered children or call the children "left" and "right" (numbers are
better because the rotation operations can be genericised easily).
An implementation can have a "parent" link at each node, or use a
temporary stack, or neither, as a stack/"parent" link is not needed
for insertion. Both "parent" links and a stack make the implementation
substantially more complex in different ways. (My sample code includes
both implementations.)

I dug through this confusion by drawing parts of the trees on paper, using 
Graphviz to plot trees, and adding test procedures which checked the
properties of the tree after each operation, generating exceptions if
anything was amiss. Tests involve randomly adding and removing
elements and checking results against data structures in the standard
library. Visual Studio's debugger is quite acceptable,
though no conventional debugger really competes with a reversible
debugger.



# Day 6

[Link to problem](https://adventofcode.com/2019/day/6)

These two problems are not difficult to solve in most languages,
but they're hard to solve in Rust, because the obvious solutions involve a
tree data structure.

There's a famous book, 
[Learn Rust With Entirely Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/).
This book exists because new Rust programmers are bound to have problems using
pointers, because they'll expect to be able to use them in something like the
same way they work in _almost every other programming language_. They might try to
write a tree data structure, like the one needed for this AoC problem, and hit lots
of compile errors even when trying to do something very simple, such as determining
the depth of a node, which would be easy in a C-like language
(e.g.  `while(a) { a=a->parent; count++; }`). In order to understand
what is wrong, the new Rust programmer will try to simplify the code. The end result
is the simplest data structure involving pointers: a linked list.

A crucial rule in Rust is that you can only have one copy of each pointer at any time.
Safety is assured by preventing any situation where more than one copy can exist: if your
code creates copies, that's a compile error.

This rules out lots of interesting data structures, including doubly-linked lists and
trees where there are both parent-child and child-parent references. Actually, such things
can be created in Rust, but you have to wrap the pointers in something that shifts the
necessary safety checks to runtime, such as the `Rc` (reference count) container. The syntax
for using `Rc` and associated containers such as `Weak` and `RefCell` is mind-bending to a
beginner. Reading the linked list book helps a lot.

In this exercise I initially tried to write the code as I would write it in Python or C.
I was able to make it work, but I was unhappy with both the first and second solutions,
because all of the pointer operations were a horrendous mess of `borrow` and `downgrade`
and `clone`. The compiler accepted it, and it produced the correct answers, but it was
terrible code - very hard to understand what is happening. Could it really
be so difficult to implement something so simple?

The lesson I really learned from this is that, in Rust, you should really try to avoid
using pointers as much as you can. Actually, this is a lot easier than it sounds, because
references can be used in many places where pointers would be needed in other languages.
I was able to do all of the AoC 2022 problems in Rust without using pointers, and this
problem can also be solved like that (my third attempt does this).

But of course I did want to return to the problem, so I re-read the linked list book,
finishing it this time. I now think I have a better solution that uses pointers and
is based on a much better understanding of what `Rc` and `RefCell` do and how the referenced
elements can be borrowed from them.  Something using a `HashMap` and referencing parents by
name is easier to follow, I think.


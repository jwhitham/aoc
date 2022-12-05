# Day 6

[Link to problem](https://adventofcode.com/2019/day/6)

Trees. These two problems are not difficult to solve in most languages,
but they're rendered extraordinarily hard by trying to solve them in Rust.

There's a famous book, [https://rust-unofficial.github.io/too-many-lists/](Learn
Rust With Entirely Too Many Linked Lists). I didn't feel that I needed to start
learning Rust at the "implement a linked list" level, but my attitude soon changed
when I realised just how difficult it actually is to use pointers in Rust. If
you have trouble writing any data structure that involves pointers, the obvious
thing to do is to try to write a simpler data structure - and the simplest data
structure involving pointers is a linked list. Naturally, it is extremely
hard to work with linked lists in Rust.

The crucial rule in Rust is that you can only have one copy of a pointer.
Safety is assured by preventing any situation where more than one copy can exist, and
the compiler does this for you. Pointers can be borrowed and moved, but not copied.
This rules out lots of interesting data structures, leaving you with singly-linked
lists and trees where the edges only point away from the root. If you happen to want
anything else, you can use reference counting (explicitly), or be unsafe, or follow the common
piece of Rust advice, which is "You don't need that!" And indeed, you don't! A simple way to
implement this AoC problem is to refer to all nodes by name and store them all in
a HashMap - that way, no pointers are needed at all. However, it feels very
limiting to be forced to use that sort of solution just because anything else is
"too hard".

I think I need to return to the linked lists book. My first attempt at part 1 used
reference counting and was only slightly hard to write, but the cycles between the tree
nodes (parent/child) would prevent the memory ever being freed. A poor solution.

My second attempt used weak references for links in the tree. It works but the complexity
is crazy. What a C programmer might write in one line, namely `while(a) { a=a->parent; count++; }`
had somehow exploded into a large subprogram filled with type declarations that would
make typical Ada programs seem terse. Though Rust does have type inference, you may
need explicit type declarations anyway, and when dealing with reference-counted
pointers there are a lot of intermediate types: Rc, Weak, RefMut, RefCell, Option...
These add much verbosity and there is a sense that Rust itself is punishing
naughty programmers for using pointers.

Part 2's implementation was quite similar to part 1's. Again, it works, but it's verbose,
filled with explicit types and sequences of "borrow", "clone", "unwrap".. can it really
be so difficult to implement something so simple? I feel that the code ends up being
much harder to understand.


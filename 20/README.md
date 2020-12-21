
# Day 20 - Modula-2

[Link to problem](https://adventofcode.com/2020/day/20)

I have not written a substantial program in 
[Modula-2](https://www.modula2.org/) for
almost 30 years - but I did use a similar language, Ada,
for seven years in my previous job. Back in the 80s I was
using a Modula-2 compiler from JPI, later Topspeed; now I have
used the [XDS compiler](https://github.com/excelsior-oss/xds)
which proved to be an excellent, professional product, very
helpful in pointing out my mistakes, and with a nice 
MS-DOS style debugger too! I had to
[refer to this tutorial](https://www.modula2.org/tutor/) many times
to remind myself of the language.

In this case I don't think the AOC problem was especially hard
since the tile edges matched unambiguously. I was expecting
something like an earlier problem where the puzzle had to be
gradually solved, because only a few pairs of edges had an
unambiguous match. Luckily not. I took my time over the problem
anyway because I was enjoying using Modula-2 again.

It's definitely simpler than Ada. The two languages are
modular in the sense that the code is broken down into packages,
each of which has externally-visible elements and a hidden
implementation. This idea has really caught on outside of
the C/C++ black hole. The two languages also have very
strong type systems which allow a lot of static and runtime
checking - in particular, it is rare to use generic "int" types
when you use these languages properly. More usually, the
programmer uses specific types which are exactly suited to
whatever they contain: for instance, if you have a tile coordinate
that is always in the range 1..10, then you can define this in the
language, and then the compiler and the runtime will both
check for overflows. Most languages do not have anything like this.
Ada is stricter about requiring type casting; Modula-2 seems to
do this more implicitly.

Ada has lots more features. One of these is a feature for templates
(named generics) which would have been useful in this problem because
a single tile and a whole image could have been represented by
the same code, with single methods for rotating and flipping.
This feature might be in some Modula-2 extensions, but it's not
in the subset of the language that I know. This is probably
the main Ada feature that I would miss, if writing more Modula-2,
though I might also miss the ability to exit early from a FOR loop.

I worked on an Ada code coverage tool for years and years, and every
new Ada standard added more special cases that were somewhat convenient
for the programmer, but were hard to support correctly and sometimes
appeared to go against the spirit of the language. For instance,
it became possible to put executable code in package specifications,
i.e. the externally visible part. I found myself sympathising with
the criticisms of Tony Hoare, when he complained that the language 
[was too complex](http://zoo.cs.yale.edu/classes/cs422/2011/bib/hoare81emperor.pdf):
and that was in the early 80s. The complexity may have proved
fatal to that language, which ended up only being used in one
industry. However, Modula-2 was also not very successful, despite
being simpler and supported by less expensive tools. Perhaps nothing
could really have stood up to C.




# Day 15 - Groovy

[Link to problem](https://adventofcode.com/2020/day/15)

This time I have used Groovy. Groovy is a nice scripting language based on
Java - the two integrate well, and it is a great use of the JVM. The language
is much more like Python than Java. You can specify types, or the language
can infer them.

Unfortunately Groovy's main use case seems to be Jenkins pipelines,
and there, the language is severely nerfed by the limitations of the
environment. In particular, the CSP transform applied by Jenkins introduces
an enormous slowdown, and using any substantial algorithm or even library code
is quite painful. This is a pity: the language is fast and flexible
when running normally within the JVM.

I think there may be a better solution for part 2, but I was not able to
find it. The sequence does not repeat, though it does
repeatedly return to zero and then progress upwards through small numbers
until reaching a large number (not seen before), which then returns to zero.
I was not able to see any pattern that might allow a faster solution.
My program uses a map (i.e. dictionary) to store the last index where each
number was stored. There is no need to actually store the sequence, just
to iterate to the required index.


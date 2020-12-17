
# Day 16 - Kotlin

[Link to problem](https://adventofcode.com/2020/day/16)

This time I have used Kotlin. Similar to Groovy, this language targets the
JVM, though unlike Groovy it can also compile to native code. It is more
ambitious than Groovy, aiming to be a complete Java replacement and more -
it also compiles to native code.

I found the language to be well-designed and very easy to use within JetBrains IDEA.
The problem could be expressed in a fairly minimal and intuitive way without
making it obscure, and the input parsing code was also easy to write because
I could use powerful string handling functions. I liked the ability to explicitly
declare constants and immutable data structures.

The ability to compile to native code is not always useful, even for small
programs. While the code itself is portable, the libraries are mostly not,
and the ability to recompile a program for a different platform depends on
whether its libraries are available. In Kotlin there is a common function library
containing some I/O functions which are available on both the JVM and for
native builds, but the I/O facilities
here are extremely limited, and opening a file is one thing that cannot be
done without importing some non-portable library. As I used the java.io functions,
my program cannot be compiled for x86.


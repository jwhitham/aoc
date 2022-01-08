"""
This is my initial working solution to the problem, made without
looking at any other solutions.

Many false starts here. I expected that the state of the registers
would collapse to a relatively small number of possibilities after
some inputs had been read, but in fact that only happens in cases
where the input is leading towards the correct answer of zero, and
unless you already know that a particular "branch" should never be taken,
you don't know that you can exclude these. I did decode the program,
converted it to Python, simplified it by hand, reconstructed the
"if" statements etc. and still did not get this.

The key insight was that the z register holds a sort of stack and
each part of the program either pushes or pops from this, thus
matching one input against another. This simple behaviour is
obfuscated in various ways, not least that if the input doesn't match,
the pop is instead a push.

I solved the problem backwards, starting at the expected result
(zero) and finding values that match. This avoids the explosion
in possible values of z which results from solving it forwards.
I still have some assumptions about the input:
* division by (at most) 26
* the program can be divided into 14 blocks, one per input,
  and only the "z" register is "live" between the blocks
so my plan here will be totally defeated by a different input structure.

Usually with these AoC problems you can produce a program which
works for any valid input but in this case that doesn't seem to be
possible and I did't like that. In part 2, most AoC puzzles punish you 
for making assumptions about the input, but in this puzzle you are
instead rewarded for hard-coding assumptions such as "the subprogram
for each input digit is always the same except for three constants".
I'm not sure how someone leaps to the key insight. Perhaps if you have
written a key generator?

I thought for a while that there could be a nasty trap for Python
users in the problem description. How many Python users are
aware that Python division rounds towards -infinity ("floor division")
rather than the more common method (rounding towards zero)?
However it seems that negative numbers are not involved in division
here so this is not relevant.


"""


import typing
import sys
import itertools

# run preprocess.py and then pythonise.py first

from pythonised import *


def conv(l):
    i = 0
    for x in l:
        i *= 10
        i += x
    return i

def main(part1):
    halfway = {}
    rmax = 0
    if part1:
        input_range = range(1, 10)
    else:
        input_range = range(9, 0, -1)

    expect_z_out = {0: []}
    for step in [calc13, calc12, calc11, calc10, calc9, calc8, calc7, calc6,
                 calc5, calc4, calc3, calc2, calc1, calc0]:

        next_z_out = {}
        rmax = (max(expect_z_out) + 1) * 26
        for z_in in range(rmax + 1):
            for i in input_range:
                try:
                    z_out = step(i, z_in)
                except Invalid:
                    continue

                if z_out in expect_z_out:
                    next_z_out[z_in] = [i] + expect_z_out[z_out]

        expect_z_out = next_z_out
        print(len(expect_z_out), flush=True)

    found = expect_z_out[0]

    if part1:
        print("part 1:", conv(found))
    else:
        print("part 2:", conv(found))

if __name__ == "__main__":
    main(True)
    main(False)

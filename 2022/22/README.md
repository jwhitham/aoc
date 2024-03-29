# Day 22 

[Link to problem](https://adventofcode.com/2022/day/22)

Mind-bending cube-folding puzzle.

For me, there was no shortcut to solving this. I think that I could have solved it faster
if I had manually translated the input file into 3D form by working out the rotation
for each face, but then, that solution would only work for one input. That's arguably
good enough, but I knew I would not be happy with it.

For a while I tried to use polar coordinates to represent the problem, hoping that these
would make it easier to cross from one face to another, but they don't actually make it
easier to deal with the effects of folding.

I finally made progress by translating the input into voxels, assuming that the
first face in the input file is the top of the cube.

To deal with the folding, I needed to store two 3D vectors per face. One vector represents
the effect of rightwards movement in the 2D puzzle input, which could actually correspond
to movement in any of six directions in 3D. The other vector represents downwards movement
in the 2D puzzle input. The crucial insight is that folding means that one of these vectors
rotates by 90 degrees around the other. The direction of the rotation is whichever direction
causes the new face to be part of the cube. Having a model cube (a cardboard box) was helpful
in realising this. I found it very hard to visualise the problem in my head or on paper.

It also helped to draw the voxel model. I suppose I could have used some 3D rendering
tool here, but I just drew 2D slices for simplicity, and this was good enough.
Looking at the voxels and comparing them to the model cube helped reveal bugs.
Usually one side was flipped wrongly.

One clunky part of the implementation is the code for moving from one face to another
while following the path. It searches both ways in all three dimensions for a voxel
on another face. The new direction could be determined directly, but this would mean
figuring out the right 3D vector rotation again.

My fear now is that a further puzzle will involve folding hypercubes or more complex 3D shapes.




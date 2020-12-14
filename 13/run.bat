@echo off

j:\D_Compiler\dmd2\windows\bin\dmd -O part1.d
j:\D_Compiler\dmd2\windows\bin\dmd -O part2.d
part1 < input
part2 < input


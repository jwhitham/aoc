#!/bin/bash -xe

/j/GHDL/0.37-mingw32-mcode/bin/ghdl.exe -a part1.vhdl set_population.vhdl question_counter.vhdl
/j/GHDL/0.37-mingw32-mcode/bin/ghdl.exe -e part1
/j/GHDL/0.37-mingw32-mcode/bin/ghdl.exe -r part1

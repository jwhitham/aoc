#!/bin/bash -xe

/j/GHDL/0.37-mingw32-mcode/bin/ghdl.exe -a part2.vhdl set_population.vhdl question_counter_part_2.vhdl
/j/GHDL/0.37-mingw32-mcode/bin/ghdl.exe -e part2
/j/GHDL/0.37-mingw32-mcode/bin/ghdl.exe -r part2

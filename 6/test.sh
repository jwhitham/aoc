#!/bin/bash -xe

/j/GHDL/0.37-mingw32-mcode/bin/ghdl.exe -a test.vhdl set_population.vhdl question_counter.vhdl
/j/GHDL/0.37-mingw32-mcode/bin/ghdl.exe -e test
/j/GHDL/0.37-mingw32-mcode/bin/ghdl.exe -r test

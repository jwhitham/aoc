#!/bin/bash -xe

/j/xds/bin/XDS-x86/bin/xc =make test.mod -NOOPTIMIZE
./test.exe > t.txt
grep ^OK t.txt
echo OK

/j/xds/bin/XDS-x86/bin/xc =make part1.mod -NOOPTIMIZE
./part1.exe > part1.html

/j/xds/bin/XDS-x86/bin/xc =make part2.mod -NOOPTIMIZE
./part2.exe > part2.txt

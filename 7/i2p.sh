#!/bin/bash -xe

convert_i2p2()
{
    sed -e 's/^\(.* bag\)s* contain \(.* bags*\)\.$/data(\1,[\2])./' < $1 \
            | tr ' ' '_' \
            | sed -e 's/_*\([0-9][0-9]*\)_\([^,]*bag\)s*/record(\1,\2)/g' > ${1}.pl
}

convert_i2p2 example_input
convert_i2p2 example_input_2
convert_i2p2 input

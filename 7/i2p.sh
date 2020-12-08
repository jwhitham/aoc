#!/bin/bash -xe

convert_i2p()
{
    sed -e 's/^\(.* bags*\) contain \(.* bags*\)\.$/data(\1,[\2])./' < $1 \
            | tr ' ' '_' \
            | sed -e 's/bags*/bag/g' \
            | sed -e 's/_*[0-9][0-9]*_//g' > $1.pl
}

convert_i2p example_input
convert_i2p input


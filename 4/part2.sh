#!/bin/bash

reset_fields()
{
    byr=0
    iyr=0
    eyr=0
    hgt=0
    hcl=0
    ecl=0
    pid=0
    cid=0
    begin=0
}

check_fields()
{
    begin=1
    egrep -q '\<byr:(19[2-9][0-9]|200[012])\>' <<< "$1" && byr=1
    egrep -q '\<iyr:(201[0-9]|2020)\>' <<< "$1" && iyr=1
    egrep -q '\<eyr:(202[0-9]|2030)\>' <<< "$1" && eyr=1
    egrep -q '\<hgt:(1[5-8][0-9]cm|19[0-3]cm|59in|6[0-9]in|7[0-6]in)\>' <<< "$1" && hgt=1
    egrep -q '\<hcl:#[0-9a-f]{6}\>' <<< "$1" && hcl=1
    egrep -q '\<ecl:(amb|blu|brn|gry|grn|hzl|oth)\>' <<< "$1" && ecl=1
    egrep -q '\<pid:[0-9]{9}\>' <<< "$1" && pid=1
}

validate_fields()
{
    if test $begin -ne 0
    then
        if test $byr -eq 1 && \
            test $iyr -eq 1 && \
            test $eyr -eq 1 && \
            test $hgt -eq 1 && \
            test $hcl -eq 1 && \
            test $ecl -eq 1 && \
            test $pid -eq 1
        then
            echo valid
            valid_count=$(( $valid_count + 1 ))
        else
            echo invalid
        fi
    fi
}

check_file()
{
    valid_count=0
    reset_fields
    dos2unix input
    while read line
    do
        if test "$line" = ""
        then
            validate_fields
            reset_fields
            echo "$line"
        else
            check_fields "$line"
            echo "$line"
        fi
    done < input
    validate_fields
    echo $valid_count
}

check_file


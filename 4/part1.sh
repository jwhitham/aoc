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

check_field()
{
    egrep -q '\<'$2':' <<< "$1" && eval "$2=1"
}

check_fields()
{
    begin=1
    check_field "$1" byr
    check_field "$1" iyr
    check_field "$1" eyr
    check_field "$1" hgt
    check_field "$1" hcl
    check_field "$1" ecl
    check_field "$1" pid
    check_field "$1" cid
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


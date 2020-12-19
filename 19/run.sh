#!/bin/bash -xe

gcc -o input_to_lex_yacc.exe input_to_lex_yacc.c -g -Wall
./input_to_lex_yacc $1
flex lex.l
bison -d yacc.y
gcc -o parser.exe yacc.tab.c lex.yy.c parser.c -g -Wall
./parser $1


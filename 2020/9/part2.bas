search%=88311122
REM search%=127
wsize%=1000
total%=0

fd=OPENIN "input.txt"
DIM window%(wsize% - 1)
index%=0
REPEAT
    PROC_readline(fd)
UNTIL EOF#fd
CLOSE#fd

PRINT "did not find anything"
PRINT "read",total%
*BYE

DEF PROC_readline(fd)
    LOCAL line$
    INPUT#fd,line$
    line$=FN_strip$(line$)
    IF line$<>"" THEN PROC_add_item(VAL(line$))
ENDPROC

DEF PROC_add_item(new%)
    total%=total% + 1
    index%=(index% + 1) MOD wsize%
    window%(index%) = new%

    LOCAL index2%
    LOCAL sum%
    LOCAL i%

    PRINT index%,new%
    index2%=index%
    sum%=new%
    FOR i%=0 TO total% - 1
        index2%=(index2% + wsize% - 1) MOD wsize%
        sum%=sum% + window%(index2%)
        IF sum%=search% THEN PROC_detect_solution(i%)
        IF sum%>=search% THEN i%=total%
    NEXT
ENDPROC

DEF PROC_detect_solution(range_size%)

    LOCAL index2%
    LOCAL sum%
    LOCAL i%
    LOCAL small%
    LOCAL big%

    sum%=0
    index2%=index%
    small%=search%
    big%=0
    FOR i%=0 TO (range_size% + 1)
        sum%=sum% + window%(index2%)
        IF window%(index2%)>big% THEN big%=window%(index2%)
        IF window%(index2%)<small% THEN small%=window%(index2%)
        index2%=(index2% + wsize% - 1) MOD wsize%
    NEXT
    PRINT "big",big%
    PRINT "small",small%
    PRINT "both",small% + big%
    IF sum%<>search% THEN PRINT "bad",sum% ELSE PRINT "ok"
    *BYE
ENDPROC

DEF FN_strip$(line$)
    LOCAL done%
    LOCAL l$
    LOCAL r$
    done%=FALSE
    REPEAT
        l$=LEFT$(line$,1)
        IF (l$=" " OR l$=CHR$(13) OR l$=CHR$(10)) THEN line$=RIGHT$(line$,LEN(line$)-1) ELSE done%=TRUE
    UNTIL done%
    done%=FALSE
    REPEAT
        r$=RIGHT$(line$,1)
        IF r$=" " OR r$=CHR$(13) OR r$=CHR$(10) THEN line$=LEFT$(line$,LEN(line$)-1) ELSE done%=TRUE
    UNTIL done%
=line$

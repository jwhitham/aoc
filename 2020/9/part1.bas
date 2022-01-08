PROC_test(25, "input.txt")
PRINT "entire file is valid"
PRINT "read",total%
*BYE

DEF PROC_test(new_wsize%, new_filename$)
    wsize%=new_wsize%
    total%=0
    fd=OPENIN new_filename$
    DIM window$(wsize% - 1)
    DIM pairs$((wsize% * (wsize% - 1)) - 1)
    index%=0
    REPEAT
        PROC_readline(fd)
    UNTIL EOF#fd
    CLOSE#fd
ENDPROC

DEF PROC_readline(fd)
    LOCAL line$
    INPUT#fd,line$
    line$=FN_strip$(line$)
    IF line$<>"" THEN PROC_add_item(line$)
ENDPROC

DEF PROC_add_item(new$)
    total%=total% + 1
    IF total%>wsize% THEN PROC_check_item(new$)
    window$(index%) = new$

    LOCAL index2%
    LOCAL i%
    index2%=index% * (wsize% - 1)

    FOR i%=0 TO (wsize% - 1)
        IF i%<>index% THEN pairs$(index2%)=FN_add$(window$(index%), window$(i%)): index2%=index2% + 1
    NEXT

    index%=(index% + 1) MOD wsize%
ENDPROC

DEF PROC_check_item(new$)
    LOCAL i%
    LOCAL j%
    LOCAL valid%
    LOCAL pair%
    valid%=FALSE
    PRINT new$
    FOR i%=0 TO ((wsize% - 1) * wsize%) - 1
        IF pairs$(i%)=new$ THEN valid%=TRUE
    NEXT
    IF NOT valid% THEN PROC_detect_invalid(new$)
ENDPROC

DEF PROC_detect_invalid(new$)
    PRINT "invalid number:",new$," on line",total%
    *BYE
ENDPROC

DEF FN_add$(a$, b$)
    LOCAL v%
    LOCAL out$
    v%=0
    out$=""

    REPEAT
        v%=VAL(RIGHT$(a$,1)) + VAL(RIGHT$(b$,1)) + v%
        a$=LEFT$(a$,LEN(a$) - 1)
        b$=LEFT$(b$,LEN(b$) - 1)
        out$=STR$(v% MOD 10) + out$
        v%=v% DIV 10
    UNTIL a$="" AND b$=""
    IF v%<>0 THEN out$=STR$(v% MOD 10) + out$
=out$        

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

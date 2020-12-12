               JOB  TEST1.S 12/12/20 10:24:45                              -8685
     *
               CTL       6611  *6=16,000C;6=16,000T;1=OBJDECK;,1=MODADD
     *   1         2         3         4         5         6         7         8
     *78901234567890123456789012345678901234567890123456789012345678901234567890
     * label   | op | OPERATION                                         |xxxxxxx

     * Advent of Code 2020 day 11 - example input
     * 
               ORG  87
     X1        DSA  0                  index register 1
               ORG  92
     X2        DSA  0                  index register 2
               ORG  97
     X3        DSA  0                  index register 3
               ORG  100 

     * Entry point
     INIT      B    START

     * Invariants
     INVAR     DCW  @I@
     HEADMS    DCW  @0000000000000000@
     WIDTH     DCW  000
     HEIGHT    DCW  000
     SPARE1    DCW  000
     SPARE2    DCW  000
     GROUP     DCW  @"@                    
     ZERO      DCW  000
     ONE       DCW  001

     * Variables
     UNSTAB    DCW  0    
     CUR       DCW  @X@
     NBR       DCW  @A@
               DCW  @B@
               DCW  @C@
               DCW  @D@
               DCW  @E@
               DCW  @F@
               DCW  @G@
               DCW  @H@
     LAST      DCW  @X@     * Must be 'X' (sentinel value)
     SCNT      DCW  0
     RESULT    DCW  000
     HEIGPP    DCW  000
     LINNUM    DCW  000

     * Print area: data written here may be printed
               ORG  200
     PRINTS    DCW  @ @
               ORG  220
     PRINTM    DC   @ @
               ORG  332
     PRINTE    DC   @ @

               ORG  350
     LINE1     DC   @.@
               ORG  400
     LINE2     DC   @.@
               ORG  450
     LINE3     DC   @.@
               ORG  500
     LINE4     DC   @.@
               ORG  550

     * Start of code
     * Reset printable area
     START     CS   PRINTE
               CS
               SW   PRINTS
     
     * template GROUP mark written
               MZ   @.@,GROUP
               SW   GROUP

     * Assume stable:
     REPEAT    MN   @0@,UNSTAB

     * Read invariants from first tape
               RWD  1
               RTW  1,INVAR

     * Print message in header
               MCW  HEADMS,PRINTM
               W
               CS   PRINTM
               SW   PRINTS

     * Write invariants to second tape
               RWD  2
               WTW  2,INVAR

     * Load initial lines
               RTW  1,LINE2&1
               RTW  1,LINE3&1
               SW   LINE1
               SW   LINE2
               SW   LINE3

     * First line: copy to tape, then replace group mark with final dot
               MCW  ZERO,X1
               A    WIDTH,X1
               A    @1@,X1
               SBR  X2,LINE2&X1

               MN   GROUP,0&X2
               MZ   GROUP,0&X2
               SW   0&X2
               WTW  2,LINE2&1

               MN   @.@,0&X2
               MZ   @.@,0&X2
               CW   0&X2
               MCW  0&X2,PRINTM
               W

     * Second line: remove group mark, add final dot
               SBR  X2,LINE3&X1
               MN   @.@,0&X2
               MZ   @.@,0&X2
               CW   0&X2

               MCW  ZERO,LINNUM
               MCW  ZERO,RESULT

     * Enter iterative process for each line
     NEWLIN    MCW  ZERO,X1
               A    WIDTH,X1
               SBR  X2,LINE1&X1
               SBR  X3,LINE2&X1
               MCW  1&X3,1&X2
               SBR  X2,LINE2&X1
               SBR  X3,LINE3&X1
               MCW  1&X3,1&X2

     * Load line: add final dot
               RTW  1,LINE3&1
               MCW  ZERO,X1
               A    WIDTH,X1
               A    @1@,X1
               SBR  X2,LINE3&X1
               MN   @.@,0&X2
               MZ   @.@,0&X2
               CW   0&X2

               MCW  ZERO,X1
     * Enter iterative process for each column
     NEWCOL    SBR  X2,LINE2&X1
               SBR  X3,LINE4&X1
               MN   1&X2,CUR
               MZ   1&X2,CUR
               MN   CUR,1&X3
               MZ   CUR,1&X3
               C    CUR,@.@
               BE   NXTCOL

     * Look at neighbouring occupied seats
     * Collect neighbours into a linear array
     * northwest
               SBR  X3,LINE1&X1
               MN   0&X3,NBR&1
               MZ   0&X3,NBR&1             
     * north
               MN   1&X3,NBR&2
               MZ   1&X3,NBR&2
     * northeast
               MN   2&X3,NBR&3
               MZ   2&X3,NBR&3
     * west
               SBR  X3,LINE2&X1
               MN   0&X3,NBR&4
               MZ   0&X3,NBR&4
     * east
               MN   2&X3,NBR&5
               MZ   2&X3,NBR&5
     * southwest
               SBR  X3,LINE3&X1
               MN   0&X3,NBR&6
               MZ   0&X3,NBR&6
     * south
               MN   1&X3,NBR&7
               MZ   1&X3,NBR&7
     * southeast
               MN   2&X3,NBR&0
               MZ   2&X3,NBR&0

     * Count the number of adjacent occupied seats
               MCW  ZERO,X3
               SBR  X3,NBR&X3
               MCW  @0@,SCNT
     * # - occupied before
     * X - end of NBR array (sentinel)
     CSEATS    MN   0&X3,CUR
               MZ   0&X3,CUR
               A    ONE,X3
               BCE  OCC,CUR,#
               BCE  CSEATD,CUR,X
               B    CSEATS
     OCC       A    @1@,SCNT
               B    CSEATS
     
     * Done counting seats
     CSEATD    C    @3@,SCNT
               BH   MANY
     * 0..3 adjacent seats are occupied
               C    @0@,SCNT
               BE   NONE
     * 1..3 adjacent seats are occupied: no state change
               B    NXTCOL
     
     * 0 adjacent seats are occupied: becomes #
     NONE      SBR  X3,LINE4&X1
               MN   @#@,1&X3
               MZ   @#@,1&X3
               MN   @1@,UNSTAB
               B    NXTCOL
     
     * 4..8 adjacent seats are occupied: becomes L
     MANY      SBR  X3,LINE4&X1
               MN   @L@,1&X3
               MZ   @L@,1&X3
               MN   @1@,UNSTAB

     * Next column or next line?
     NXTCOL    A    @1@,X1
               C    WIDTH,X1
               BU   NEWCOL

     * End of line: write the new line to tape
     NXTLIN    MCW  ZERO,X1
               A    WIDTH,X1
               A    @1@,X1
               SBR  X3,LINE4&X1
               MN   GROUP,0&X3
               MZ   GROUP,0&X3
               SW   0&X3
               WTW  2,LINE4&1

     * Then print the new line
               MN   @.@,0&X3
               MZ   @.@,0&X3
               CW   0&X3
               MCW  0&X3,PRINTM
               W

     * Final line? or finished?
               A    ONE,LINNUM
               C    HEIGHT,LINNUM
               BU   NEWLIN

     * Write a final empty line to the tape
               MCW  ZERO,X1
               A    WIDTH,X1
               A    @1@,X1
               SBR  X3,LINE3&X1
               MN   GROUP,0&X3
               MZ   GROUP,0&X3
               SW   0&X3
               WTW  2,LINE3&1

     * Then print the final line
               MN   @.@,0&X3
               MZ   @.@,0&X3
               CW   0&X3
               MCW  0&X3,PRINTM
               W

     * Rewind the tapes and copy tape 2 -> tape 1
               RWD  1
               RWD  2
               RTW  2,INVAR
               WTW  1,INVAR

               MCW  HEIGHT,HEIGPP
               A    @2@,HEIGPP

               MCW  ZERO,LINNUM
               MCW  ZERO,X1
               A    WIDTH,X1
     COPY      RTW  2,LINE4&1
               SBR  X3,LINE4&X1
               MN   GROUP,1&X3
               MZ   GROUP,1&X3
               SW   1&X3
               WTW  1,LINE4&1

     * Count occupied seats
               MCW  ZERO,X2
     CCOLS     SBR  X3,LINE4&X2
               MN   0&X3,CUR
               MZ   0&X3,CUR
               C    @#@,CUR
               BU   NOTOCC

               A    ONE,RESULT    * occupied

     NOTOCC    A    @1@,X2
               C    WIDTH,X2
               BU   CCOLS

     * Final line? or finished?
               A    @1@,LINNUM
               C    HEIGPP,LINNUM
               BU   COPY
    
     * Print count of occupied seats
               CS   PRINTM
               SW   PRINTS
               MCW  RESULT,PRINTM
               W
               CS   PRINTM
               SW   PRINTS

     * Repeat if unstable
               C    @0@,UNSTAB
               BU   REPEAT

     * Otherwise finished - halt

               H    START
               B    START

               END  START

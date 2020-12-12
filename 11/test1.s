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
     LINNUM    DCW  0
     CUR       DCW  @X@
     CUR2      DCW  @X@
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
     
     * GROUP mark written
               MZ   @.@,GROUP
               SW   GROUP

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
               A    @1@,LINNUM
               C    HEIGHT,LINNUM
               BU   NEWLIN

    

     
               H    START
               B    START

               END  START

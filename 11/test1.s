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
               DCW  @0123456789ABCDEF@
     WIDTH     DCW  012
     HEIGHT    DCW  012
     SIZE      DCW  144     * WIDTH * HEIGHT
     SIZE1     DCW  120     * WIDTH * (HEIGHT - 2)
     GROUP     DCW  @"@                    
     ZERO      DCW  000
     ONE       DCW  001

     * Variables
     UNSTAB    DCW  0    
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

     * Data area (represents the seating area)
     FIELD0    DCW  0
     FIELD1    DCW  @............@
               DCW  @.L.LL.LL.LL.@
               DCW  @.LLLLLLL.LL.@
               DCW  @.L.L.L..L...@
               DCW  @.LLLL.LL.LL.@
               DCW  @.L.LL.LL.LL.@
               DCW  @.L.LLLLL.LL.@
               DCW  @...L.L......@
               DCW  @.LLLLLLLLLL.@
               DCW  @.L.LLLLLL.L.@
               DCW  @.L.LLLLL.LL.@
               DCW  @............@

    
     * Reset printable area
     START     CS   PRINTE
               CS
               SW   PRINTS
     
     * GROUP mark written
               MZ   @.@,GROUP
               SW   GROUP

     * Output to tape
               RWD  1
               WTW  1,INVAR         * header
               MCW  ZERO,X1
     WTAPE     SBR  X2,FIELD0&X1
               SBR  X3,FIELD0&X1
               A    WIDTH,X2
               MZ   GROUP,0&X2      * group mark at end of line
               MN   GROUP,0&X2
               SW   0&X2
               WTW  1,2&X3          * write to tape
               MZ   @.@,0&X2        * dot at end of line
               MN   @.@,0&X2
               CW   0&X2
               A    WIDTH,X1
               C    SIZE,X1
               BU   WTAPE

     * Reset the puzzle
               MCW  ZERO,X1
     RPUZ      SBR  X2,FIELD0&X1
               MN   0&X2,CUR
               MZ   0&X2,CUR
               BCE  DOT,CUR,.
               MN   @L@,0&X2
               MZ   @L@,0&X2
     DOT       A    ONE,X1
               C    SIZE,X1
               BU   RPUZ
     
     * Ready: Start iterating
     REPEAT    SW   PRINTS

     * Are we stable yet? Assume yes
               MN   @0@,UNSTAB
     
     * Go to the next state
               MCW  ZERO,X1
     ITER      SBR  X2,FIELD1&X1
               A    ONE,X2
     * Current cell is at X2 - does it represent floor space?
               MN   0&X2,CUR
               MZ   0&X2,CUR
               C    CUR,@.@
               BE   NSEAT
     
     * It represents a seat - so we need to decide what happens next
     * Collect occupied seats into a linear array
     * northwest
               SBR  X3,FIELD0&X1
               MN   0&X3,NBR&1
               MZ   0&X3,NBR&1             
     * north
               MN   1&X3,NBR&2
               MZ   1&X3,NBR&2
     * northeast
               MN   2&X3,NBR&3
               MZ   2&X3,NBR&3
     * west
               A    WIDTH,X3
               MN   0&X3,NBR&4
               MZ   0&X3,NBR&4
     * east
               MN   2&X3,NBR&5
               MZ   2&X3,NBR&5
     * southwest
               A    WIDTH,X3
               MN   0&X3,NBR&6
               MZ   0&X3,NBR&6
     * south
               MN   1&X3,NBR&7
               MZ   1&X3,NBR&7
     * southeast
               MN   2&X3,NBR&0
               MZ   2&X3,NBR&0

     * Count the number of occupied seats
               MCW  ZERO,X3
               SBR  X3,NBR&X3
               MCW  @0@,SCNT
     * F - occupied before, unoccupied now
     * # - occupied before and now
     * X - end of NBR array
     CSEATS    MN   0&X3,CUR2
               MZ   0&X3,CUR2
               A    ONE,X3
               BCE  OCC,CUR2,F
               BCE  OCC,CUR2,#
               BCE  CSEATD,CUR2,X
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
               B    NSEAT 
     
     * 0 adjacent seats are occupied
     * Rules:
     *  #    -> # (still occupied)
     *  else -> O (became occupied)
     NONE      C    @#@,CUR
               BE   NSEAT
               MN   @O@,0&X2
               MZ   @O@,0&X2
               MN   @1@,UNSTAB
               B    NSEAT
     
     * 4..8 adjacent seats are occupied
     * Rules:
     *  #    -> F (became vacant)
     *  else -> L (still vacant)
     MANY      C    @#@,CUR
               BE   VAC
               B    NSEAT
     VAC       MN   @F@,0&X2
               MZ   @F@,0&X2
               MN   @1@,UNSTAB

     * Go to the next seat (or space on the floor)                             
     NSEAT     A    ONE,X1
               C    SIZE1,X1
               BU   ITER   
     
     * Turn all temporary values into their permanent form
     *  F  -> L
     *  O  -> #
     *  #  -> #
     *  L  -> L
               MCW  ZERO,X1
     PERM      SBR  X2,FIELD0&X1
               MN   0&X2,CUR
               MZ   0&X2,CUR
               BCE  MAKEF,CUR,F
               BCE  MAKEO,CUR,O
               B    NPERM
     MAKEF     MN   @L@,0&X2
               MZ   @L@,0&X2
               B    NPERM
     MAKEO     MN   @#@,0&X2
               MZ   @#@,0&X2
     NPERM     A    ONE,X1
               C    SIZE,X1
               BU   PERM
     
     * Print out the current state of the field
               MCW  ZERO,X1
     OUTLP     SBR  X2,FIELD1&X1
               MCW  0&X2,PRINTM              
               W
               A    WIDTH,X1
               C    SIZE,X1
               BU   OUTLP
     * Print a blank line
               CS   PRINTM
               W

     * Are we stable yet?
               C    @0@,UNSTAB
               BU   REPEAT
           
     * We're stable! How many occupied seats?
               MCW  ZERO,X1
               MCW  ZERO,RESULT
     CALC      SBR  X2,FIELD0&X1
               MN   0&X2,CUR
               MZ   0&X2,CUR
               BCE  UNEMPT,CUR,#
               B    NCALC
     UNEMPT    A    ONE,RESULT
     NCALC     A    ONE,X1
               C    SIZE,X1
               BU   CALC
     
               CS   PRINTM
               MCW  RESULT,PRINTM
               W
     
               H    START
               B    START
               END  START

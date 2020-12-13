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
     UNSTAB    DCW  0           * Nonzero if there was a change
     WIDTH2    DCW  000         * Width + 2
     CURCNT    DCW  0           * Current tape 2 value for the cell: . or 0..9 (see table)
     *                          *  .   floor space
     *                          *  0   occupied with 0 people visible from west, northwest, north or northeast
     *                          *  1   occupied with 1 person " " " " "
     *                          *  2   occupied with 2 people " " " " "
     *                          *  3   occupied with 3 people " " " " "
     *                          *  4   occupied with 4 people " " " " "
     *                          *  5   unoccupied with 0 people " " " " "
     *                          *  6   unoccupied with 1 person " " " " "
     *                          *  7   unoccupied with 2 people " " " " "
     *                          *  8   unoccupied with 3 people " " " " "
     *                          *  9   unoccupied with 4 people " " " " "
     CURCEL    DCW  @X@         * Current tape 1 cell value: . or # or L
     TMP       DCW  0
     WEST      DCW  0
     RESULT    DCW  00000
     LINNUM    DCW  000

     * Print area: data written here may be printed
               ORG  200
     PRINTS    DCW  @ @
               ORG  240
     PRINTM    DC   @ @
               ORG  300
     DATIN     DC   @.@
               ORG  420
     DATOUT    DC   @.@
               ORG  540
     NTHWST    DC   @.@
               ORG  660
     NTH       DC   @.@
               ORG  880
     NTHEST    DC   @.@
               ORG  999


     * Start of code
     * Reset printable area
     START     CS   PRINTM
               SW   PRINTS
     
     * template GROUP mark written
               MZ   @.@,GROUP
               SW   GROUP

     * Assume stable:
     REPEAT    MN   @0@,UNSTAB
               MCW  @00000@,RESULT

     * Both tapes to the beginning
               RWD  1
               RWD  2

     * Read invariants from first tape
               RTW  1,INVAR

     * Print message in header
               MCW  HEADMS,PRINTM
               W
               CS   PRINTM
               SW   PRINTS

     * Compute WIDTH + 2
               MCW  WIDTH,WIDTH2
               A    ONE,WIDTH2
               A    ONE,WIDTH2

     * Ignore first line
               RTW  1,DATIN&0


     * BEGIN NORTH TO SOUTH PASS
     * Here is the setup for the pass
               MCW  ZERO,LINNUM

     * Clear out previous line flags: NTHWST, NTH, NTHEAST
     * Clear the characters at -1 and +1 for each array too
     * so that later passes can rely on these being 0.
               MCW  ZERO,X1
     NTSCLR    SBR  X2,NTHWST-1&X1
               MN   @0@,0&X2
               MZ   @0@,0&X2
               CW   0&X2
               SBR  X2,NTH-1&X1
               MN   @0@,0&X2
               MZ   @0@,0&X2
               CW   0&X2
               SBR  X2,NTHEST-1&X1
               MN   @0@,0&X2
               MZ   @0@,0&X2
               CW   0&X2
               A    ONE,X1
               C    WIDTH2,X1
               BU   NTSCLR

     * The north to south pass begins
     * Load line from tape 1
     NTSPAS    RTW  1,DATIN&0
               MCW  @0@,WEST

     * BEGIN WEST TO EAST SUBPASS
               MCW  ZERO,X1
     WTEPAS    SBR  X2,DATIN&X1
               MN   0&X2,CURCEL
               MZ   0&X2,CURCEL
               C    @#@,CURCEL
               BE   WTESET
               C    @L@,CURCEL
               BE   WTESET

     * This cell is floor space
     * Tape 2 code is '.':  data2[y][x] = 0
               SBR  X2,DATOUT&X1
               MN   @.@,0&X2
               MZ   @.@,0&X2

     * Propagate northeast flag
               SBR  X2,NTHEST-1&X1
               MN   0&X2,1&X2
               MZ   0&X2,1&X2
               B    WTENXT
               
     * This cell is not floor space
     * How many people are visible?
     WTESET    MCW  WEST,CURCNT         * add west
               SBR  X2,NTHWST&X1        * add northwest
               MN   0&X2,TMP
               MZ   0&X2,TMP
               A    TMP,CURCNT
               SBR  X2,NTH&X1           * add north
               MN   0&X2,TMP
               MZ   0&X2,TMP
               A    TMP,CURCNT
               SBR  X2,NTHEST&X1        * add northeast
               MN   0&X2,TMP
               MZ   0&X2,TMP
               A    TMP,CURCNT
               MCW  @1@,WEST            * west flag set if occupied
               C    @#@,CURCEL
               BE   WTEOCC

     * Add 5 if the cell is unoccupied and clear west flag
               A    @5@,CURCNT
               MCW  @0@,WEST            * west flag cleared if not occupied

     WTEOCC    SBR  X2,NTH&X1           * copy west flag to north flag
               MN   WEST,0&X2
               MZ   WEST,0&X2
               SBR  X2,NTHEST-1&X1      * copy west flag to northeast flag
               MN   WEST,0&X2
               MZ   WEST,0&X2

     * Value for this cell is stored
               SBR  X2,DATOUT&X1
               MN   CURCNT,0&X2
               MZ   CURCNT,0&X2

     * Next iteration of west to east subpass?
     WTENXT    A    ONE,X1
               C    WIDTH,X1
               BU   WTEPAS

     * BEGIN EAST TO WEST SUBPASS
               MCW  WIDTH,X1
     ETWPAS    S    ONE,X1
               MZ   ZERO,X1-2
               MZ   ZERO,X1-1
               MZ   ZERO,X1
               SBR  X2,DATIN&X1
               MN   0&X2,CURCEL
               MZ   0&X2,CURCEL
               C    @#@,CURCEL
               BE   ETWOCC          * occupied
               C    @L@,CURCEL
               BE   ETWVAC          * vacant

     * The cell is empty: propagate northwest flag
               SBR  X2,NTHWST-1&X1
               MN   0&X2,1&X2
               MZ   0&X2,1&X2
               B    ETWNXT
     
     * The cell is occupied - set northwest flag
     ETWOCC    SBR  X2,NTHWST&X1
               MN   @1@,0&X2
               MZ   @1@,0&X2
               B    ETWNXT

     * The cell is vacant - clear northwest flag
     ETWVAC    SBR  X2,NTHWST&X1
               MN   @0@,0&X2
               MZ   @0@,0&X2

     ETWNXT    C    ZERO,X1
               BU   ETWPAS

     * Completed WTE and ETW subpasses - write to tape 2
               MCW  WIDTH,X1
               SBR  X2,DATOUT&X1
               MN   GROUP,0&X2
               MZ   GROUP,0&X2
               SW   0&X2
               WTW  2,DATOUT

     * Repeat until north to south pass is complete
               A    ONE,LINNUM
               C    HEIGHT,LINNUM
               BU   NTSPAS


               H    START
               B    START

               END  START

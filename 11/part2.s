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

     * Tape 1: input tape (read only)
     * Tape 2: work tape (write during north-south pass, read during south-north pass)
     * Tape 3: work tape (write during south-north pass and setup, read during north-south pass)
     * Tape 4: log tape for debugging (write only)

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
     CURCNT    DCW  0           * Current tape 2 value for the cell (valid between north-south pass and south-north pass)
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
     CURCEL    DCW  @X@         * Current tape 3 cell value
     *                          *  .   floor space
     *                          *  O   became occupied (during south-north pass only)
     *                          *  #   occupied
     *                          *  V   became unoccupied (during south-north pass only)
     *                          *  L   unoccupied
     CURCPY    DCW  0           * copy of tape 2 value (before modification in south-north pass)
     TMP       DCW  0
     WEST      DCW  0
     EAST      DCW  0
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
     STHWST    DC   @.@
               ORG  660
     NTH       DC   @.@
     STH       DC   @.@
               ORG  880
     NTHEST    DC   @.@
     STHEST    DC   @.@
               ORG  999


     * Start of code
     * Reset printable area
     START     CS   PRINTM
               SW   PRINTS
     
     * template GROUP mark written
               MZ   @.@,GROUP
               SW   GROUP

     * all tapes to the beginning
               RWD  1
               RWD  2
               RWD  3
               RWD  4

     * Read invariants from input tape
               RTW  1,INVAR

     * Print message in header
               MCW  HEADMS,PRINTM
               W
               CS   PRINTM
               SW   PRINTS

     * Ignore first line in input tape (don't change the format!)
               RTW  1,DATIN&0

     * Copy input tape 1 -> work tape 3
               MCW  ZERO,LINNUM
     COPY      RTW  1,DATIN&0
               MCW  WIDTH,X1
               SBR  X2,DATIN&X1
               MN   GROUP,0&X2
               MZ   GROUP,0&X2
               SW   0&X2
               WTW  3,DATIN

               A    ONE,LINNUM
               C    HEIGHT,LINNUM
               BU   COPY

     * Now we are done with tape 1
               RWD  1

     * Assume stable:
     REPEAT    MN   @0@,UNSTAB
               MCW  @00000@,RESULT

     * work tapes to the beginning
               RWD  2
               RWD  3

     * Compute WIDTH + 2
               MCW  WIDTH,WIDTH2
               A    ONE,WIDTH2
               A    ONE,WIDTH2



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
     * Load line from tape 3
     NTSPAS    RTW  3,DATIN&0
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
               MN   1&X2,0&X2
               MZ   1&X2,0&X2
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
               SBR  X2,NTHWST&X1
               MN   0&X2,1&X2
               MZ   0&X2,1&X2
               B    ETWNXT
     
     * The cell is occupied - set northwest flag
     ETWOCC    SBR  X2,NTHWST&X1
               MN   @1@,1&X2
               MZ   @1@,1&X2
               B    ETWNXT

     * The cell is vacant - clear northwest flag
     ETWVAC    SBR  X2,NTHWST&X1
               MN   @0@,1&X2
               MZ   @0@,1&X2

     ETWNXT    C    ZERO,X1
               BU   ETWPAS

     * Completed WTE and ETW subpasses - write to tape 2
               MCW  WIDTH,X1
               SBR  X2,DATOUT&X1
               MN   GROUP,0&X2
               MZ   GROUP,0&X2
               SW   0&X2
               WTW  2,DATOUT
               WTW  4,DATOUT  * And log to tape 4

     * Repeat until north to south pass is complete
               A    ONE,LINNUM
               C    HEIGHT,LINNUM
               BU   NTSPAS

     * BEGIN SOUTH TO NORTH PASS
     * Here is the setup for the pass
               MCW  ZERO,LINNUM

     * Clear out previous line flags: STHWST, STH, STHEAST
     * Clear the characters at -1 and +1 for each array too
     * so that later passes can rely on these being 0.
               MCW  ZERO,X1
     STNCLR    SBR  X2,STHWST-1&X1
               MN   @0@,0&X2
               MZ   @0@,0&X2
               CW   0&X2
               SBR  X2,STH-1&X1
               MN   @0@,0&X2
               MZ   @0@,0&X2
               CW   0&X2
               SBR  X2,STHEST-1&X1
               MN   @0@,0&X2
               MZ   @0@,0&X2
               CW   0&X2
               A    ONE,X1
               C    WIDTH2,X1
               BU   STNCLR

     * The south to north pass begins
     * Load line from tape 2
     STNPAS    BSP  2
               RTW  2,DATIN&0
               BSP  2
               MCW  @0@,EAST

     * BEGIN EAST TO WEST SUBPASS
               MCW  WIDTH,X1
     ETWPA2    S    ONE,X1
               MZ   ZERO,X1-2
               MZ   ZERO,X1-1
               MZ   ZERO,X1
               SBR  X2,DATIN&X1
               MN   0&X2,CURCNT
               MZ   0&X2,CURCNT
               MCW  CURCNT,CURCPY
               C    @.@,CURCNT          * detect tape 2 code '.' -> floor
               BU   ETWSE2

     * This cell is floor space
               SBR  X2,DATOUT&X1
               MN   @.@,0&X2
               MZ   @.@,0&X2

     * Propagate southwest flag
               SBR  X2,STHWST&X1
               MN   0&X2,1&X2
               MZ   0&X2,1&X2
               B    ETWNX2
               
     * This cell is not floor space
     * How many people are visible?
     ETWSE2    C    @5@,CURCNT
               BL   NOSUB
               S    @5@,CURCNT          * subtract 5 to get number of people
               MZ   @0@,CURCNT

     NOSUB     A    EAST,CURCNT         * add east
               SBR  X2,STHWST&X1        * add southwest
               MN   0&X2,TMP
               MZ   0&X2,TMP
               A    TMP,CURCNT
               SBR  X2,STH&X1           * add south
               MN   0&X2,TMP
               MZ   0&X2,TMP
               A    TMP,CURCNT
               SBR  X2,STHEST&X1        * add southeast
               MN   0&X2,TMP
               MZ   0&X2,TMP
               A    TMP,CURCNT

               SBR  X2,DATIN&X1         * write total number of people to DATIN
               MN   CURCNT,0&X2
               MZ   CURCNT,0&X2

               C    @4@,CURCPY          * detect tape 2 code 5..9 -> unoccupied
               BH   ETWVA2

     * Cell is occupied (currently)
               MCW  @1@,EAST            * east flag set if occupied

               C    @5@,CURCNT          * detect less than 5 visible
               BL   KEEP1

     * Cell is occupied currently and 5 or more people are visible -> become unoccupied
               SBR  X2,DATOUT&X1
               MN   @V@,0&X2            * DATOUT: temporarily V (became vacant)
               MZ   @V@,0&X2
               MN   @1@,UNSTAB
               B    ETWFL2
    
     * Cell is occupied currently and 4 or fewer people are visible -> stay occupied
     KEEP1     SBR  X2,DATOUT&X1
               MN   @#@,0&X2            * DATOUT: still # (occupied)
               MZ   @#@,0&X2
               A    @00001@,RESULT
               B    ETWFL2

     * Cell is unoccupied (currently)
     ETWVA2    MCW  @0@,EAST            * east flag cleared if not occupied

               C    @0@,CURCNT          * detect 0 people visible
               BU   KEEP2

     * Cell is unoccupied currently and 0 people are visible -> become occupied
               SBR  X2,DATOUT&X1
               MN   @O@,0&X2            * DATOUT: temporarily O (became occupied)
               MZ   @O@,0&X2
               MN   @1@,UNSTAB
               A    @00001@,RESULT
               B    ETWFL2

     * Cell is unoccupied currently and 1 or more people are visible -> stay unoccupied
     KEEP2     SBR  X2,DATOUT&X1
               MN   @L@,0&X2            * DATOUT: still L (unoccupied)
               MZ   @L@,0&X2

     * Propagate flags
     ETWFL2    SBR  X2,STH&X1           * copy east flag to south flag
               MN   EAST,0&X2
               MZ   EAST,0&X2
               SBR  X2,STHWST&X1        * copy east flag to southwest flag
               MN   EAST,1&X2
               MZ   EAST,1&X2

     * Next iteration of east to west subpass?
     ETWNX2    C    ZERO,X1
               BU   ETWPA2

     * BEGIN WEST TO EAST SUBPASS
               MCW  ZERO,X1
     WTEPA2    SBR  X2,DATOUT&X1
               MN   0&X2,CURCEL
               MZ   0&X2,CURCEL
               C    @O@,CURCEL
               BE   WTEBO2          * became occupied
               C    @#@,CURCEL
               BE   WTESO2          * still occupied
               C    @V@,CURCEL
               BE   WTEBV2          * became vacant
               C    @L@,CURCEL
               BE   WTESV2          * still vacant

     * The cell is empty: propagate southeast flag
               SBR  X2,STHEST-1&X1
               MN   1&X2,0&X2
               MZ   1&X2,0&X2
               B    WTENX2
    
     * The cell was occupied and became vacant
     WTEBV2    SBR  X2,STHEST-1&X1
               MN   @1@,0&X2
               MZ   @1@,0&X2
               SBR  X2,DATOUT&X1
               MN   @L@,0&X2
               MZ   @L@,0&X2
               B    WTENX2

     * The cell was occupied and still is
     WTESO2    SBR  X2,STHEST-1&X1
               MN   @1@,0&X2
               MZ   @1@,0&X2
               B    WTENX2

     * The cell was vacant and became occupied
     WTEBO2    SBR  X2,STHEST-1&X1
               MN   @0@,0&X2
               MZ   @0@,0&X2
               SBR  X2,DATOUT&X1
               MN   @#@,0&X2
               MZ   @#@,0&X2
               B    WTENX2

     * The cell was vacant and still is
     WTESV2    SBR  X2,STHEST-1&X1
               MN   @0@,0&X2
               MZ   @0@,0&X2

     * Next west-to-east iteration
     WTENX2    A    ONE,X1
               C    WIDTH,X1
               BU   WTEPA2

     * Completed ETW and WTE subpasses - write to tape 3
               MCW  WIDTH,X1
               SBR  X2,DATOUT&X1
               MN   GROUP,0&X2
               MZ   GROUP,0&X2
               SW   0&X2
               BSP  3
               WTW  3,DATOUT
               BSP  3

     * Also log to tape 4
               MCW  WIDTH,X1
               SBR  X2,DATIN&X1
               MN   GROUP,0&X2
               MZ   GROUP,0&X2
               SW   0&X2
               WTW  4,DATIN

     * Repeat until south to north pass is complete
               A    ONE,LINNUM
               C    HEIGHT,LINNUM
               BU   STNPAS

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

               H    START
               B    START

               END  START

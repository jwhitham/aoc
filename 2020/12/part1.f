C AOC2020 puzzle 12 part 1
        PROGRAM part1
 501        FORMAT(A1,I9)
 601        FORMAT("opcode=",A1," operand=",I9)
 801        FORMAT("end at east=",I9," north=",I9," manhattan=",I9)
 901        FORMAT("unknown input",A1,I9)
 902        FORMAT("unknown direction",I5)

            INTEGER direction, east, north
            CHARACTER opcode
            INTEGER operand

            direction = 90
            east = 0
            north = 0

            DO
                READ(*,501,END=800,ERR=900) opcode,operand
                SELECT CASE(opcode)
                    CASE ('N')
                        north = north + operand
                    CASE ('S')
                        north = north - operand
                    CASE ('E')
                        east = east + operand
                    CASE ('W')
                        east = east - operand
                    CASE ('L')
                        direction = MOD(direction + 360 - operand, 360)
                    CASE ('R')
                        direction = MOD(direction + operand, 360)
                    CASE ('F')
                        SELECT CASE(direction)
                            CASE (90)
                                east = east + operand
                            CASE (180)
                                north = north - operand
                            CASE (270)
                                east = east - operand
                            CASE (0)
                                north = north + operand
                            CASE DEFAULT
                                WRITE(*,902) direction
                                STOP
                        END SELECT
                    CASE DEFAULT
                        WRITE(*,901) opcode,operand
                        STOP
                END SELECT
            END DO

C       normal exit
 800        WRITE(*,801) east,north,ABS(east) + ABS(north)
            STOP
C       input error
 900        WRITE(*,901) opcode,operand
            STOP
        END

C AOC2020 puzzle 12 part 2

        PROGRAM part2
 501        FORMAT(A1,I9)
 601        FORMAT("opcode=",A1," operand=",I9)
 801        FORMAT("end at east=",I9," north=",I9," manhattan=",I9)
 901        FORMAT("unknown input",A1,I9)
            IMPLICIT none
            INTEGER wp_east, wp_north
            INTEGER ship_east, ship_north
            INTEGER mh
            CHARACTER opcode
            INTEGER operand

            wp_east = 10
            wp_north = 1
            ship_east = 0
            ship_north = 0

            DO
                READ(*,501,END=800,ERR=900) opcode,operand
                SELECT CASE(opcode)
                    CASE ('N')
                        wp_north = wp_north + operand
                    CASE ('S')
                        wp_north = wp_north - operand
                    CASE ('E')
                        wp_east = wp_east + operand
                    CASE ('W')
                        wp_east = wp_east - operand
                    CASE ('L')
                        operand = MOD(360 - operand, 360)
                        CALL wp_rotate(operand,wp_east,wp_north)
                    CASE ('R')
                        operand = MOD(operand, 360)
                        CALL wp_rotate(operand,wp_east,wp_north)
                    CASE ('F')
                        ship_east = ship_east + (wp_east * operand)
                        ship_north = ship_north + (wp_north * operand)
                    CASE DEFAULT
                        WRITE(*,901) opcode,operand
                        STOP
                END SELECT
            END DO

C       normal exit
 800        mh = (ABS(ship_east) + ABS(ship_north))
            WRITE(*,801) ship_east,ship_north,mh
            STOP
C       input error
 900        WRITE(*,901) opcode,operand
            STOP
        END

        SUBROUTINE wp_rotate_90(wp_east,wp_north)
            INTEGER tmp
            INTEGER wp_east
            INTEGER wp_north
            tmp = wp_east
            wp_east = wp_north
            wp_north = -tmp
        END

        SUBROUTINE wp_rotate(direction,wp_east,wp_north)
            INTEGER direction
            INTEGER wp_east
            INTEGER wp_north
 902        FORMAT("unknown direction",I5)
            SELECT CASE(direction)
                CASE (0)
                CASE (90)
                    CALL wp_rotate_90(wp_east,wp_north)
                CASE (180)
                    CALL wp_rotate_90(wp_east,wp_north)
                    CALL wp_rotate_90(wp_east,wp_north)
                CASE (270)
                    CALL wp_rotate_90(wp_east,wp_north)
                    CALL wp_rotate_90(wp_east,wp_north)
                    CALL wp_rotate_90(wp_east,wp_north)
                CASE DEFAULT
                    WRITE(*,902) direction
                    STOP
            END SELECT
        END SUBROUTINE wp_rotate


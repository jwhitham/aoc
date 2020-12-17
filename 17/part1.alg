
INT input_grid_size = 8;
INT margin_size = 8;
INT grid_size = (margin_size * 2) + input_grid_size;
INT lower_margin = 2;
INT upper_margin = grid_size - 1;

CHAR inactive = ".";
CHAR active = "#";
CHAR activating = "A";
CHAR deactivating = "D";

MODE GRID = [grid_size, grid_size, grid_size] CHAR;
PR include "prelude" PR

PROC read_grid = GRID:
    BEGIN
        GRID grid;
        CHAR tmp;
        INT middle := (grid_size + 1) % 2;
        INT upper := grid_size + 1 - margin_size;
        
        FOR z FROM 1 TO grid_size DO
            FOR y FROM 1 TO grid_size DO
                FOR x FROM 1 TO grid_size DO
                    tmp := ".";
                    IF z = middle AND x > margin_size AND x < upper 
                    AND y > margin_size AND y < upper THEN
                        read(tmp)
                    FI;
                    grid[z, y, x] := tmp
                OD
            OD
        OD;
        grid
    END;

PROC print_grid = (GRID grid) VOID:
    BEGIN
        FOR z FROM 1 TO grid_size DO
            print("z=");
            print(z);
            print(newline);
            FOR y FROM 1 TO grid_size DO
                FOR x FROM 1 TO grid_size DO
                    print(grid[z, y, x])
                OD;
                print(newline)
            OD
        OD
    END;

PROC count_active = (GRID grid) INT:
    BEGIN
        INT count := 0;
        FOR z FROM 1 TO grid_size DO
            FOR y FROM 1 TO grid_size DO
                FOR x FROM 1 TO grid_size DO
                    IF grid[z, y, x] = active THEN
                        count := count + 1
                    FI
                OD
            OD
        OD;
        count
    END;

PROC step_grid = (REF GRID grid) BOOL:
    BEGIN
        BOOL too_big := FALSE;
        FOR z1 FROM lower_margin TO upper_margin DO
            FOR y1 FROM lower_margin TO upper_margin DO
                FOR x1 FROM lower_margin TO upper_margin DO
                    INT count := 0;
                    CHAR current_state := grid[z1, y1, x1];
                    grid[z1, y1, x1] := inactive;

                    FOR z2 FROM z1 - 1 TO z1 + 1 DO
                        FOR y2 FROM y1 - 1 TO y1 + 1 DO
                            FOR x2 FROM x1 - 1 TO x1 + 1 DO
                                IF grid[z2, y2, x2] = active
                                OR grid[z2, y2, x2] = deactivating THEN
                                    count := count + 1
                                FI
                            OD
                        OD
                    OD;
                    grid[z1, y1, x1] := current_state;
                    IF (current_state = active AND (count < 2 OR count > 3)) THEN
                        grid[z1, y1, x1] := deactivating
                    ELSE
                        IF (current_state = inactive AND count = 3) THEN
                            grid[z1, y1, x1] := activating
                        FI
                    FI
                OD
            OD
        OD;
        FOR z1 FROM lower_margin TO upper_margin DO
            FOR y1 FROM lower_margin TO upper_margin DO
                FOR x1 FROM lower_margin TO upper_margin DO
                    IF grid[z1, y1, x1] = activating THEN
                        grid[z1, y1, x1] := active;
                        IF (z1 = lower_margin
                        OR y1 = lower_margin
                        OR x1 = lower_margin
                        OR z1 = upper_margin 
                        OR y1 = upper_margin 
                        OR x1 = upper_margin) THEN
                            too_big := TRUE
                        FI
                    ELSE
                        IF grid[z1, y1, x1] = deactivating THEN
                            grid[z1, y1, x1] := inactive
                        FI
                    FI
                OD
            OD
        OD;
        too_big
    END;

GRID grid := read_grid;
FOR i FROM 1 TO 6 DO
    IF step_grid (grid) THEN
        print("Too big at step ");
        print(i);
        print(newline)
    ELSE
        print("at step ");
        print(i);
        print(newline);
        # print_grid (grid); #
        print("total active ");
        print(count_active(grid));
        print(newline)
    FI
OD


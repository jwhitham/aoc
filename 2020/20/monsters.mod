IMPLEMENTATION MODULE Monsters;

IMPORT TileSet;
IMPORT EdgeMatch;
IMPORT STextIO;

PROCEDURE CreateImage(VAR tile_set  : TileSet.TileSet;
                      VAR grid      : EdgeMatch.Grid;
                      VAR image     : Image);
    VAR gx, gy      : TileSet.GridCoord;
    VAR gx1, gy1    : TileSet.GridCoord;
    VAR gx2, gy2    : TileSet.GridCoord;
    VAR tx, ty      : TileSet.CellCoord;
    VAR ix, iy      : ImageCoord;
    VAR tile        : TileSet.TileIndex;
BEGIN
    EdgeMatch.GetGridBounds(grid, gx1, gy1, gx2, gy2);
    FOR iy := 1 TO ImageSize DO
        FOR ix := 1 TO ImageSize DO
            image[iy][ix] := Calm;
        END;
    END;
    FOR gy := gy1 TO gy2 DO
        FOR gx := gx1 TO gx2 DO
            tile := grid[gy][gx];
            iy := ((gy - gy1) * (TileSet.TileSize - 2));
            FOR ty := 2 TO TileSet.TileSize - 1 DO
                INC(iy);
                ix := ((gx - gx1) * (TileSet.TileSize - 2));
                FOR tx := 2 TO TileSet.TileSize - 1 DO
                    INC(ix);
                    IF (tile <> 0) AND tile_set.tile[tile].cell[ty][tx] THEN
                        image[iy][ix] := Wave;
                    END;
                END;
            END;
        END;
    END;
END CreateImage;

PROCEDURE Rotate(VAR input : Image);
    VAR rotated     : Image;
    VAR x1, y1      : ImageCoord;
    VAR x2, y2      : ImageCoord;
BEGIN
    FOR y1 := 1 TO ImageSize DO
        x2 := y1;
        FOR x1 := 1 TO ImageSize DO
            y2 := ImageSize + 1 - x1;
            rotated[y2][x2] := input[y1][x1];
        END;
    END;
    input := rotated;
END Rotate;

PROCEDURE Flip(VAR input : Image);
    VAR x1, y1      : ImageCoord;
    VAR x2          : ImageCoord;
    VAR tmp         : Sea;
BEGIN
    FOR y1 := 1 TO ImageSize DO
        FOR x1 := 1 TO ImageSize DIV 2 DO
            x2 := ImageSize + 1 - x1;
            tmp := input[y1][x2];
            input[y1][x2] := input[y1][x1];
            input[y1][x1] := tmp;
        END;
    END;
END Flip;

PROCEDURE FindMonstersInOneOrientation(VAR input : Image): CARDINAL;
    VAR x1, y1      : ImageCoord;
    VAR x2          : CARDINAL;
    VAR detect      : BOOLEAN;
    VAR count       : CARDINAL;
    CONST monster1 = "                  # ";
    CONST monster2 = "#    ##    ##    ###";
    CONST monster3 = " #  #  #  #  #  #   ";
BEGIN
    count := 0;
    FOR y1 := 2 TO ImageSize - 2 DO
        FOR x1 := 1 TO ImageSize + 1 - LENGTH(monster2) DO
            detect := TRUE;
            FOR x2 := 0 TO LENGTH(monster2) - 1 DO
                IF (monster2[x2] = '#') AND (input[y1][x1 + x2] <> Wave) THEN
                    detect := FALSE;
                ELSIF (monster3[x2] = '#') AND (input[y1 + 1][x1 + x2] <> Wave) THEN
                    detect := FALSE;
                ELSIF (monster1[x2] = '#') AND (input[y1 - 1][x1 + x2] <> Wave) THEN
                    detect := FALSE;
                END;
            END;
            IF detect THEN
                INC(count);
                FOR x2 := 0 TO LENGTH(monster2) - 1 DO
                    IF (monster2[x2] = '#') AND (input[y1][x1 + x2] = Wave) THEN
                        input[y1][x1 + x2] := Monster;
                    END;
                    IF (monster3[x2] = '#') AND (input[y1 + 1][x1 + x2] = Wave) THEN
                        input[y1 + 1][x1 + x2] := Monster;
                    END;
                    IF (monster1[x2] = '#') AND (input[y1 - 1][x1 + x2] = Wave) THEN
                        input[y1 - 1][x1 + x2] := Monster;
                    END;
                END;
            END;
        END;
    END;
    RETURN count;
END FindMonstersInOneOrientation;

PROCEDURE FindMonsters(VAR input : Image): CARDINAL;
    VAR i, j : CARDINAL;
    VAR count : CARDINAL;
BEGIN
    count := 0;
    FOR i := 1 TO 2 DO
        FOR j := 1 TO 4 DO
            count := FindMonstersInOneOrientation(input) + count;
            Rotate(input);
        END;
        Flip(input);
    END;
    RETURN count;
END FindMonsters;

PROCEDURE CountWaves(VAR input : Image): CARDINAL;
    VAR count   : CARDINAL;
    VAR x, y    : ImageCoord;
BEGIN
    count := 0;
    FOR y := 1 TO ImageSize DO
        FOR x := 1 TO ImageSize DO
            IF input[y][x] = Wave THEN
                INC(count);
            END;
        END;
    END;
    RETURN count;
END CountWaves;

PROCEDURE PrintImage(VAR input : Image);
    VAR x, y      : ImageCoord;
BEGIN
    FOR y := 1 TO ImageSize DO
        FOR x := 1 TO ImageSize DO
            CASE input[y][x] OF
                Wave: STextIO.WriteString('#'); |
                Calm: STextIO.WriteString('.'); |
                Monster: STextIO.WriteString('O');
            END;
        END;
        STextIO.WriteLn;
    END;
END PrintImage;

END Monsters.

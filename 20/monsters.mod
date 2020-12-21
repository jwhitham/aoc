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
            iy := 1 + ((gy - gy1) * (TileSet.TileSize - 2));
            FOR ty := 2 TO TileSet.TileSize - 1 DO
                ix := 1 + ((gx - gx1) * (TileSet.TileSize - 2));
                FOR tx := 2 TO TileSet.TileSize - 1 DO
                    IF (tile <> 0) AND tile_set.tile[tile].cell[ty][tx] THEN
                        image[iy][ix] := Wave;
                    END;
                    INC(ix);
                END;
                INC(iy);
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

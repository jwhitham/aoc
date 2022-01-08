IMPLEMENTATION MODULE TileSet;
IMPORT SeqFile;
IMPORT TextIO;
IMPORT WholeIO;
IMPORT STextIO;
IMPORT SWholeIO;
IMPORT ChanConsts;
IMPORT Strings;

PROCEDURE ReadTileSet(filename      : ARRAY OF CHAR;
                      VAR tile_set  : TileSet;
                      VAR error     : BOOLEAN);
    VAR f           : SeqFile.ChanId;
    VAR open_result : SeqFile.OpenResults;
    VAR row         : ARRAY [1 .. TileSize] OF CHAR;
    VAR tile_string : ARRAY [1 .. 5] OF CHAR;
    VAR i           : TileIndex;
    VAR x, y        : CellCoord;
    VAR number      : CARDINAL;
BEGIN
    error := FALSE;
    tile_set.max_index := 0;
    SeqFile.OpenRead(f, filename, SeqFile.text, open_result);
    IF open_result <> ChanConsts.opened THEN
        STextIO.WriteString('Open error');
        STextIO.WriteLn;
        error := TRUE;
        RETURN;
    END;
    FOR i := 1 TO (GridSize * GridSize) DO
        TextIO.ReadString(f, tile_string);
        IF NOT Strings.Equal(tile_string, "Tile ") THEN
            SeqFile.Close(f);
            IF i = 1 THEN
                STextIO.WriteString('Parsing error (Tile)');
                STextIO.WriteLn;
                error := TRUE;
            END;
            RETURN;
        END;
        WholeIO.ReadCard(f, number);
        TextIO.SkipLine(f);
        tile_set.tile[i].number := number;

        FOR y := 1 TO TileSize DO
            TextIO.ReadString(f, row);
            TextIO.SkipLine(f);
            FOR x := 1 TO TileSize DO
                IF row[x] = '#' THEN
                    tile_set.tile[i].cell[y][x] := TRUE;
                ELSIF row[x] = '.' THEN
                    tile_set.tile[i].cell[y][x] := FALSE;
                ELSE
                    SeqFile.Close(f);
                    STextIO.WriteString('Parsing error (Cell)');
                    STextIO.WriteLn;
                    error := TRUE;
                    RETURN;
                END;
            END;
        END;
        TextIO.ReadString(f, tile_string);
        IF NOT Strings.Equal(tile_string, "") THEN
            SeqFile.Close(f);
            STextIO.WriteString('Parsing error (Gap)');
            STextIO.WriteLn;
            error := TRUE;
            RETURN;
        END;
        TextIO.SkipLine(f);
        tile_set.max_index := i;
    END;
    SeqFile.Close(f);

END ReadTileSet;

PROCEDURE Rotate(VAR input : Tile);
    VAR rotated     : Tile;
    VAR x1, y1      : CellCoord;
    VAR x2, y2      : CellCoord;
BEGIN
    FOR y1 := 1 TO TileSize DO
        x2 := y1;
        FOR x1 := 1 TO TileSize DO
            y2 := TileSize + 1 - x1;
            rotated.cell[y2][x2] := input.cell[y1][x1];
        END;
    END;
    input.cell := rotated.cell;
END Rotate;

PROCEDURE Flip(VAR input : Tile);
    VAR x1, y1      : CellCoord;
    VAR x2          : CellCoord;
    VAR tmp         : BOOLEAN;
BEGIN
    FOR y1 := 1 TO TileSize DO
        FOR x1 := 1 TO TileSize DIV 2 DO
            x2 := TileSize + 1 - x1;
            tmp := input.cell[y1][x2];
            input.cell[y1][x2] := input.cell[y1][x1];
            input.cell[y1][x1] := tmp;
        END;
    END;
END Flip;

PROCEDURE PrintTile(tile : Tile);
    VAR x, y        : CellCoord;
BEGIN
    STextIO.WriteString('Tile ');
    SWholeIO.WriteCard(tile.number, 1);
    STextIO.WriteLn;
    FOR y := 1 TO TileSize DO
        FOR x := 1 TO TileSize DO
            IF tile.cell[y][x] THEN
                STextIO.WriteString('#');
            ELSE
                STextIO.WriteString('.');
            END;
        END;
        STextIO.WriteLn;
    END;
END PrintTile;

END TileSet.

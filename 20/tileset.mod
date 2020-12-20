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
    VAR x, y        : Coord;
    VAR number      : CARDINAL;
    VAR j           : CARDINAL;
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
        tile_set.tile[i].number := number;
        TextIO.SkipLine(f);
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
        FOR j := 1 TO Edges DO
            tile_set.tile[i].edge[j] := 0;
        END;
        tile_set.max_index := i;
    END;
    SeqFile.Close(f);

END ReadTileSet;

PROCEDURE Rotate(input : Tile): Tile;
    VAR rotated     : Tile;
    VAR x1, y1      : Coord;
    VAR x2, y2      : Coord;
BEGIN
    rotated := input;
    FOR y1 := 1 TO TileSize DO
        x2 := y1;
        FOR x1 := 1 TO TileSize DO
            y2 := TileSize + 1 - x1;
            rotated.cell[y2][x2] := input.cell[y1][x1];
        END;
    END;
    RETURN rotated;
END Rotate;

PROCEDURE Flip(input : Tile): Tile;
    VAR flipped     : Tile;
    VAR x1, y1      : Coord;
    VAR x2          : Coord;
BEGIN
    flipped := input;
    FOR y1 := 1 TO TileSize DO
        FOR x1 := 1 TO TileSize DO
            x2 := TileSize + 1 - x1;
            flipped.cell[y1][x2] := input.cell[y1][x1];
        END;
    END;
    RETURN flipped;
END Flip;

PROCEDURE ComputeEdges(VAR tile_set : TileSet);
    VAR i           : TileIndex;
    VAR j           : CARDINAL;
    VAR x           : Coord;
    VAR copy        : Tile;
    VAR bit         : CARDINAL;
    VAR edge_value  : CARDINAL;
BEGIN
    FOR i := 1 TO tile_set.max_index DO
        copy := tile_set.tile[i];
        FOR j := 1 TO Edges DO
            bit := 1;
            edge_value := 0;
            FOR x := 1 TO TileSize DO
                IF copy.cell[1][x] THEN
                    edge_value := edge_value + bit;
                END;
                bit := bit * 2;
            END;
            tile_set.tile[i].edge[j] := edge_value;
            copy := Rotate(copy);
            IF j = 4 THEN
                copy := Flip(copy);
            END;
        END;
    END;
END ComputeEdges;

PROCEDURE PrintTile(tile : Tile);
    VAR x, y        : Coord;
    VAR i           : CARDINAL;
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
    STextIO.WriteString('Edges');
    FOR i := 1 TO Edges DO
        STextIO.WriteString(' ');
        SWholeIO.WriteCard(tile.edge[i], 1);
    END;
    STextIO.WriteLn;
END PrintTile;

END TileSet.

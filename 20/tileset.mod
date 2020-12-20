IMPLEMENTATION MODULE TileSet;
IMPORT SeqFile;
IMPORT TextIO;
IMPORT WholeIO;
IMPORT InOut;
IMPORT ChanConsts;
IMPORT Strings;

PROCEDURE ReadTileSet(filename      : ARRAY OF CHAR;
                      VAR tile_set  : TileSet;
                      VAR error     : BOOLEAN);
    VAR f           : SeqFile.ChanId;
    VAR open_result : SeqFile.OpenResults;
    VAR row         : ARRAY [1 .. TileSize] OF CHAR;
    VAR tile_string : ARRAY [1 .. 5] OF CHAR;
    VAR i           : Index;
    VAR x, y        : Coord;
    VAR number      : CARDINAL;
BEGIN
    error := FALSE;
    tile_set.max_index := 0;
    SeqFile.OpenRead(f, filename, SeqFile.text, open_result);
    IF open_result <> ChanConsts.opened THEN
        InOut.WriteString('Open error');
        InOut.WriteLn;
        error := TRUE;
        RETURN;
    END;
    FOR i := 1 TO (GridSize * GridSize) DO
        TextIO.ReadString(f, tile_string);
        IF NOT Strings.Equal(tile_string, "Tile ") THEN
            SeqFile.Close(f);
            IF i = 1 THEN
                InOut.WriteString('Parsing error (Tile)');
                InOut.WriteLn;
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
                    InOut.WriteString('Parsing error (Cell)');
                    InOut.WriteLn;
                    error := TRUE;
                    RETURN;
                END;
            END;
        END;
        TextIO.ReadString(f, tile_string);
        IF NOT Strings.Equal(tile_string, "") THEN
            SeqFile.Close(f);
            InOut.WriteString('Parsing error (Gap)');
            InOut.WriteLn;
            error := TRUE;
            RETURN;
        END;
        TextIO.SkipLine(f);
        tile_set.max_index := i;
    END;
    SeqFile.Close(f);

END ReadTileSet;

END TileSet.

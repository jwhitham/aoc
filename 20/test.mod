MODULE Test;
IMPORT TileSet;
IMPORT EdgeMatch;
IMPORT STextIO;

VAR tile_set : TileSet.TileSet;
VAR grid     : EdgeMatch.Grid;
VAR error    : BOOLEAN;
VAR x1, y1   : TileSet.GridCoord;
VAR x2, y2   : TileSet.GridCoord;
VAR corner   : LONGREAL;

BEGIN
    TileSet.ReadTileSet("example_input", tile_set, error);
    IF error THEN
        STextIO.WriteString("error reading input");
        STextIO.WriteLn;
        RETURN;
    END;
    EdgeMatch.EdgeMatch(tile_set, grid, error);
    IF error THEN
        STextIO.WriteString("error matching edges");
        STextIO.WriteLn;
        RETURN;
    END;
    EdgeMatch.GetGridBounds(grid, x1, y1, x2, y2);
    corner := LFLOAT(tile_set.tile[grid[y1][x1]].number);
    corner := corner * LFLOAT(tile_set.tile[grid[y2][x1]].number);
    corner := corner * LFLOAT(tile_set.tile[grid[y1][x2]].number);
    corner := corner * LFLOAT(tile_set.tile[grid[y2][x2]].number);
    IF corner <> 20899048083289.0 THEN
        STextIO.WriteString("error - wrong answer (part 1)");
        STextIO.WriteLn;
        RETURN;
    END;
    STextIO.WriteString("OK");
    STextIO.WriteLn;
END Test.

MODULE Part1;
IMPORT TileSet;
IMPORT EdgeMatch;
IMPORT STextIO;
IMPORT SLongIO;

VAR tile_set : TileSet.TileSet;
VAR grid     : EdgeMatch.Grid;
VAR error    : BOOLEAN;
VAR x1, y1   : TileSet.GridCoord;
VAR x2, y2   : TileSet.GridCoord;
VAR corner   : LONGREAL;

BEGIN
    TileSet.ReadTileSet("input", tile_set, error);
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
    STextIO.WriteString('<html><body>');
    EdgeMatch.PrintGrid(tile_set, grid);
    EdgeMatch.GetGridBounds(grid, x1, y1, x2, y2);

    corner := LFLOAT(tile_set.tile[grid[y1][x1]].number);
    corner := corner * LFLOAT(tile_set.tile[grid[y2][x1]].number);
    corner := corner * LFLOAT(tile_set.tile[grid[y1][x2]].number);
    corner := corner * LFLOAT(tile_set.tile[grid[y2][x2]].number);
    STextIO.WriteLn;
    STextIO.WriteString("<p>part 1 result ");
    SLongIO.WriteFixed(corner, 0, 1);
    STextIO.WriteLn;
    STextIO.WriteString('</body></html>');
END Part1.

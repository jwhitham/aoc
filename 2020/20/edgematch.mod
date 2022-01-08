IMPLEMENTATION MODULE EdgeMatch;

FROM Storage IMPORT ALLOCATE, DEALLOCATE;
FROM SYSTEM IMPORT TSIZE;
IMPORT TileSet;
IMPORT STextIO;
IMPORT SWholeIO;

CONST
    Edges = 8;
    MaxEdgeValue = 1023;  (* (2 ** TileSize) - 1 *)
TYPE
    EdgeValue = [0 .. MaxEdgeValue];
    EdgeIndex = [1 .. Edges];
    EdgeValueList = ARRAY EdgeIndex OF EdgeValue;
    MatchListPtr = POINTER TO MatchListItem;
    MatchListItem =
        RECORD
            tile    : TileSet.TileIndex;
            next    : MatchListPtr;
        END;

    EdgeTable =
        RECORD
            match    : ARRAY EdgeValue OF MatchListPtr;
            grid     : Grid;
            tile_set : TileSet.TileSet;
        END;

PROCEDURE Push(VAR match : MatchListPtr;
               tile      : TileSet.TileIndex);
    VAR item : MatchListPtr;
BEGIN
    ALLOCATE(item, TSIZE(MatchListItem));
    item^.next := match;
    item^.tile := tile;
    match := item;
END Push;

PROCEDURE RemoveEdge(VAR match : MatchListPtr;
                     index     : TileSet.TileIndex);
    VAR item : MatchListPtr;
BEGIN
    item := match;
    IF match = NIL THEN
        RETURN;
    ELSIF item^.tile = index THEN
        match := item^.next;
        DEALLOCATE(item, TSIZE(MatchListItem));
    ELSIF item^.next <> NIL THEN
        RemoveEdge(item^.next, index);
    END;
END RemoveEdge;

PROCEDURE Pop(VAR match : MatchListPtr): TileSet.TileIndex;
    VAR item : MatchListPtr;
    VAR tile : TileSet.TileIndex;
BEGIN
    item := match;
    match := item^.next;
    tile := item^.tile;
    DEALLOCATE(item, TSIZE(MatchListItem));
    RETURN tile;
END Pop;

PROCEDURE Length(match : MatchListPtr): CARDINAL;
    VAR item  : MatchListPtr;
    VAR count : CARDINAL;
BEGIN
    item := match;
    count := 0;
    WHILE item <> NIL DO
        INC(count);
        item := item^.next;
    END;
    RETURN count;
END Length;

PROCEDURE ComputeEdges(tile : TileSet.Tile): EdgeValueList;
    VAR j           : CARDINAL;
    VAR x           : TileSet.CellCoord;
    VAR bit         : CARDINAL;
    VAR edge_value  : EdgeValueList;
BEGIN
    FOR j := 1 TO Edges DO
        bit := 1;
        edge_value[j] := 0;
        FOR x := 1 TO TileSet.TileSize DO
            IF tile.cell[1][x] THEN
                edge_value[j] := edge_value[j] + bit;
            END;
            bit := bit * 2;
        END;
        TileSet.Rotate(tile);
        IF j = 4 THEN
            TileSet.Flip(tile);
        END;
    END;
    RETURN edge_value;
END ComputeEdges;

PROCEDURE RemoveTileFromTable(VAR edge_table : EdgeTable;
                              tile           : TileSet.TileIndex);
    VAR edge_value  : EdgeValueList;
    VAR j           : EdgeIndex;
BEGIN
    edge_value := ComputeEdges(edge_table.tile_set.tile[tile]);
    FOR j := 1 TO Edges DO
        RemoveEdge(edge_table.match[edge_value[j]], tile);
    END;
END RemoveTileFromTable;

PROCEDURE PlaceTile(VAR edge_table : EdgeTable;
                    x, y           : TileSet.GridCoord;
                    tile           : TileSet.TileIndex);
BEGIN
    edge_table.grid[y][x] := tile;
    RemoveTileFromTable(edge_table, tile);
END PlaceTile;

PROCEDURE CheckAllEdges(VAR edge_table : EdgeTable;
                        x, y           : TileSet.GridCoord): BOOLEAN;
    VAR i               : TileSet.CellCoord;
    VAR north, west     : TileSet.TileIndex;
    VAR south, east     : TileSet.TileIndex;
    VAR centre          : TileSet.TileIndex;
BEGIN
    centre := edge_table.grid[y][x];
    IF centre = 0 THEN
        RETURN TRUE;
    END;
    north := edge_table.grid[y - 1][x];
    west := edge_table.grid[y][x - 1];
    south := edge_table.grid[y + 1][x];
    east := edge_table.grid[y][x + 1];

    FOR i := 1 TO TileSet.TileSize DO
        IF north <> 0 THEN
            IF edge_table.tile_set.tile[north].cell[TileSet.TileSize][i] <>
                    edge_table.tile_set.tile[centre].cell[1][i] THEN
                RETURN FALSE;
            END;
        END;
        IF west <> 0 THEN
            IF edge_table.tile_set.tile[west].cell[i][TileSet.TileSize] <>
                    edge_table.tile_set.tile[centre].cell[i][1] THEN
                RETURN FALSE;
            END;
        END;
        IF south <> 0 THEN
            IF edge_table.tile_set.tile[south].cell[1][i] <>
                    edge_table.tile_set.tile[centre].cell[TileSet.TileSize][i] THEN
                RETURN FALSE;
            END;
        END;
        IF east <> 0 THEN
            IF edge_table.tile_set.tile[east].cell[i][1] <>
                    edge_table.tile_set.tile[centre].cell[i][TileSet.TileSize] THEN
                RETURN FALSE;
            END;
        END;
    END;
    RETURN TRUE;
END CheckAllEdges;

PROCEDURE FindNextMatch(VAR edge_table : EdgeTable;
                        x1, y1         : TileSet.GridCoord);
    VAR item1, item2    : TileSet.TileIndex;
    VAR edge_value1     : EdgeValueList;
    VAR j, k            : EdgeIndex;
    VAR x2, y2          : TileSet.GridCoord;

    PROCEDURE EdgeDX(j : EdgeIndex): TileSet.GridCoord;
    BEGIN
        CASE j OF
            2,6 :   RETURN 1; |
            4,8 :   RETURN -1;
        ELSE
            RETURN 0;
        END;
    END EdgeDX;

    PROCEDURE EdgeDY(j : EdgeIndex): TileSet.GridCoord;
    BEGIN
        CASE j OF
            3,7 :   RETURN 1; |
            1,5 :   RETURN -1;
        ELSE
            RETURN 0;
        END;
    END EdgeDY;

BEGIN
    item1 := edge_table.grid[y1][x1];
    edge_value1 := ComputeEdges(edge_table.tile_set.tile[item1]);
    FOR j := 1 TO 4 DO
        IF Length(edge_table.match[edge_value1[j]]) = 1 THEN
            (* exactly one tile can fit here *)
            x2 := EdgeDX(j) + x1;
            y2 := EdgeDY(j) + y1;
            IF edge_table.grid[y2][x2] = 0 THEN
                item2 := Pop(edge_table.match[edge_value1[j]]);
                PlaceTile(edge_table, x2, y2, item2);

                (* Rotate so edges match *)
                FOR k := 1 TO Edges DO
                    IF NOT CheckAllEdges(edge_table, x2, y2) THEN
                        TileSet.Rotate(edge_table.tile_set.tile[item2]);
                        IF k = 4 THEN
                            TileSet.Flip(edge_table.tile_set.tile[item2]);
                        END;
                    END;
                END;
                FindNextMatch(edge_table, x2, y2);
            END;
        END; 
    END;
END FindNextMatch;

PROCEDURE FindFirstMatch(VAR edge_table : EdgeTable);
    VAR k           : EdgeValue;
BEGIN
    FOR k := 0 TO MaxEdgeValue DO
        IF Length(edge_table.match[k]) = 2 THEN
            (* two tiles match - place the first one *)
            PlaceTile(edge_table, 0, 0, edge_table.match[k]^.tile);
            FindNextMatch(edge_table, 0, 0);
            RETURN;
        END;
    END;
END FindFirstMatch;

PROCEDURE CheckGrid(VAR edge_table : EdgeTable): BOOLEAN;
    VAR x, y            : TileSet.GridCoord;
    VAR error           : BOOLEAN;
BEGIN
    error := FALSE;
    FOR y := MIN(TileSet.GridCoord) + 1 TO MAX(TileSet.GridCoord) DO
        FOR x := MIN(TileSet.GridCoord) + 1 TO MAX(TileSet.GridCoord) DO
            IF (NOT error) AND (NOT CheckAllEdges(edge_table, x, y)) THEN
                STextIO.WriteString('Edge error on edge of ');
                SWholeIO.WriteInt(x, 1);
                STextIO.WriteString(',');
                SWholeIO.WriteInt(y, 1);
                STextIO.WriteLn;
                error := TRUE;
            END;
        END;
    END;
    IF error THEN
        STextIO.WriteString('Edges do not line up!');
    END;
    RETURN NOT error;
END CheckGrid;

PROCEDURE GetGridBounds(VAR grid       : Grid;
                        VAR x1, y1     : TileSet.GridCoord;
                        VAR x2, y2     : TileSet.GridCoord);
    VAR x, y        : TileSet.GridCoord;
BEGIN
    x1 := MAX(TileSet.GridCoord);
    y1 := MAX(TileSet.GridCoord);
    x2 := MIN(TileSet.GridCoord);
    y2 := MIN(TileSet.GridCoord);
    FOR y := MIN(TileSet.GridCoord) TO MAX(TileSet.GridCoord) DO
        FOR x := MIN(TileSet.GridCoord) TO MAX(TileSet.GridCoord) DO
            IF grid[y][x] <> 0 THEN
                IF x < x1 THEN
                    x1 := x;
                END;
                IF x > x2 THEN
                    x2 := x;
                END;
                IF y < y1 THEN
                    y1 := y;
                END;
                IF y > y2 THEN
                    y2 := y;
                END;
            END;
        END;
    END;
END GetGridBounds;

PROCEDURE PrintGrid(VAR tile_set : TileSet.TileSet;
                    VAR grid     : Grid);
    VAR x, y        : TileSet.GridCoord;
    VAR x1, y1      : TileSet.GridCoord;
    VAR x2, y2      : TileSet.GridCoord;
BEGIN
    STextIO.WriteString('<table>');
    GetGridBounds(grid, x1, y1, x2, y2);
    FOR y := y1 TO y2 DO
        STextIO.WriteString('<tr>');
        FOR x := x1 TO x2 DO
            STextIO.WriteString('<td><pre>');
            IF grid[y][x] <> 0 THEN
                TileSet.PrintTile(tile_set.tile[grid[y][x]]);
            END;
            STextIO.WriteString('</pre></td>');
        END;
        STextIO.WriteString('</tr>');
    END;
    STextIO.WriteString('</table>');
    STextIO.WriteLn;
END PrintGrid;


PROCEDURE EdgeMatch(VAR tile_set : TileSet.TileSet;
                    VAR grid     : Grid;
                    VAR error    : BOOLEAN);
    VAR edge_table  : EdgeTable;
    VAR edge_value  : EdgeValueList;
    VAR x, y        : TileSet.GridCoord;
    VAR i           : TileSet.TileIndex;
    VAR j           : EdgeIndex;
    VAR k           : EdgeValue;
BEGIN
    error := FALSE;
    edge_table.tile_set := tile_set;
    FOR y := MIN(TileSet.GridCoord) TO MAX(TileSet.GridCoord) DO
        FOR x := MIN(TileSet.GridCoord) TO MAX(TileSet.GridCoord) DO
            edge_table.grid[y][x] := 0;
        END;
    END;
    FOR k := 0 TO MaxEdgeValue DO
        edge_table.match[k] := NIL;
    END;
    FOR i := 1 TO edge_table.tile_set.max_index DO
        edge_value := ComputeEdges(edge_table.tile_set.tile[i]);
        FOR j := 1 TO Edges DO
            Push(edge_table.match[edge_value[j]], i);
        END;
    END;
    FindFirstMatch(edge_table);
    IF CheckGrid(edge_table) THEN
        tile_set := edge_table.tile_set;
        grid := edge_table.grid;
    ELSE
        error := TRUE;
    END;
END EdgeMatch;

END EdgeMatch.


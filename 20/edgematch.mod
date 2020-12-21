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
            match   : ARRAY EdgeValue OF MatchListPtr;
            grid    : ARRAY TileSet.GridCoord OF
                        ARRAY TileSet.GridCoord OF TileSet.TileIndex;
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

PROCEDURE RotateFlipForEdges(VAR tile   : TileSet.Tile;
                             count      : EdgeIndex);
    VAR j   : EdgeIndex;
BEGIN
    IF count = 1 THEN
        RETURN;
    END;
    FOR j := 1 TO count - 1 DO
        TileSet.Rotate(tile);
        IF j = 4 THEN
            TileSet.Flip(tile);
        END;
    END;
END RotateFlipForEdges;

PROCEDURE RemoveTileFromTable(VAR edge_table : EdgeTable;
                              VAR tile_set   : TileSet.TileSet;
                              tile           : TileSet.TileIndex);
    VAR edge_value  : EdgeValueList;
    VAR j           : EdgeIndex;
BEGIN
    edge_value := ComputeEdges(tile_set.tile[tile]);
    FOR j := 1 TO Edges DO
        RemoveEdge(edge_table.match[edge_value[j]], tile);
    END;
END RemoveTileFromTable;

PROCEDURE PlaceTile(VAR edge_table : EdgeTable;
                    VAR tile_set   : TileSet.TileSet;
                    x, y           : TileSet.GridCoord;
                    tile           : TileSet.TileIndex);
BEGIN
    STextIO.WriteString('place tile ');
    SWholeIO.WriteCard(tile, 1);
    STextIO.WriteString(' at ');
    SWholeIO.WriteInt(x, 1);
    STextIO.WriteString(',');
    SWholeIO.WriteInt(y, 1);
    STextIO.WriteLn;

    tile_set.tile[tile].x := x;
    tile_set.tile[tile].y := y;
    tile_set.tile[tile].placed := TRUE;
    edge_table.grid[y][x] := tile;
    RemoveTileFromTable(edge_table, tile_set, tile);
END PlaceTile;

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

PROCEDURE FindNextMatch(VAR edge_table : EdgeTable;
                        VAR tile_set   : TileSet.TileSet;
                        x1, y1         : TileSet.GridCoord);
    VAR item1, item2    : TileSet.TileIndex;
    VAR edge_value1     : EdgeValueList;
    VAR edge_value2     : EdgeValueList;
    VAR j, k            : EdgeIndex;
    VAR rotation        : EdgeIndex;
    VAR x2, y2          : TileSet.GridCoord;
BEGIN
    item1 := edge_table.grid[y1][x1];
    edge_value1 := ComputeEdges(tile_set.tile[item1]);
    FOR j := 1 TO 4 DO
        IF Length(edge_table.match[edge_value1[j]]) = 1 THEN
            (* exactly one tile can fit here *)
            x2 := EdgeDX(j) + x1;
            y2 := EdgeDY(j) + y1;
            IF edge_table.grid[y2][x2] = 0 THEN
                item2 := Pop(edge_table.match[edge_value1[j]]);
                PlaceTile(edge_table, tile_set, x2, y2, item2);

                (* Rotate so edges match *)
                edge_value2 := ComputeEdges(tile_set.tile[item2]);
                rotation := 1;
                FOR k := 1 TO Edges DO
                    IF edge_value2[k] = edge_value1[1] THEN
                        rotation := k;
                    END;
                END;
                CASE j OF
                    1:  TileSet.Rotate(tile_set.tile[item2]);
                        TileSet.Rotate(tile_set.tile[item2]);
                        TileSet.Flip(tile_set.tile[item2]); |
                    2:  |
                    3:  |
                    4:  TileSet.Rotate(tile_set.tile[item2]);
                        TileSet.Rotate(tile_set.tile[item2]);
                        TileSet.Rotate(tile_set.tile[item2]);
                END;
                RotateFlipForEdges(tile_set.tile[item2], rotation);
                FindNextMatch(edge_table, tile_set, x2, y2);
            END;
        END; 
    END;
END FindNextMatch;

PROCEDURE FindFirstMatch(VAR edge_table : EdgeTable;
                         VAR tile_set   : TileSet.TileSet);
    VAR k           : EdgeValue;
BEGIN
    FOR k := 0 TO MaxEdgeValue DO
        IF Length(edge_table.match[k]) = 2 THEN
            (* two tiles match - place the first one *)
            PlaceTile(edge_table, tile_set, 0, 0, edge_table.match[k]^.tile);
            FindNextMatch(edge_table, tile_set, 0, 0);
            RETURN;
        END;
    END;
END FindFirstMatch;

PROCEDURE CheckGrid(VAR edge_table : EdgeTable;
                    VAR tile_set   : TileSet.TileSet);
    VAR x, y            : TileSet.GridCoord;
    VAR i               : TileSet.CellCoord;
    VAR north, west     : TileSet.TileIndex;
    VAR centre          : TileSet.TileIndex;
    VAR error           : BOOLEAN;
BEGIN
    error := FALSE;
    FOR y := MIN(TileSet.GridCoord) + 1 TO MAX(TileSet.GridCoord) DO
        FOR x := MIN(TileSet.GridCoord) + 1 TO MAX(TileSet.GridCoord) DO
            centre := edge_table.grid[y][x];
            IF centre <> 0 THEN
                north := edge_table.grid[y - 1][x];
                west := edge_table.grid[y][x - 1];

                FOR i := 1 TO TileSet.TileSize DO
                    IF (north <> 0) AND NOT error THEN
                        IF tile_set.tile[north].cell[TileSet.TileSize][i] <>
                                tile_set.tile[centre].cell[1][i] THEN
                            STextIO.WriteString('Edge error on north edge of ');
                            SWholeIO.WriteInt(x, 1);
                            STextIO.WriteString(',');
                            SWholeIO.WriteInt(y, 1);
                            STextIO.WriteLn;
                            error := TRUE;
                        END;
                    END;
                    IF (west <> 0) AND NOT error THEN
                        IF tile_set.tile[west].cell[i][TileSet.TileSize] <>
                                tile_set.tile[centre].cell[i][1] THEN

                            STextIO.WriteString('Edge error on west edge of ');
                            SWholeIO.WriteInt(x, 1);
                            STextIO.WriteString(',');
                            SWholeIO.WriteInt(y, 1);
                            STextIO.WriteLn;
                            error := TRUE;
                        END;
                    END;
                END;
            END;
        END;
    END;
    IF error THEN
        STextIO.WriteString('Edges do not line up!');
    END;
END CheckGrid;

PROCEDURE GetGridBounds(VAR edge_table : EdgeTable;
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
            IF edge_table.grid[y][x] <> 0 THEN
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

PROCEDURE PrintGrid(VAR edge_table : EdgeTable;
                    VAR tile_set   : TileSet.TileSet);
    VAR x, y        : TileSet.GridCoord;
    VAR x1, y1      : TileSet.GridCoord;
    VAR x2, y2      : TileSet.GridCoord;
BEGIN
    GetGridBounds(edge_table, x1, y1, x2, y2);
    STextIO.WriteString('<html><body><table>');
    FOR y := y1 TO y2 DO
        STextIO.WriteString('<tr>');
        FOR x := x1 TO x2 DO
            STextIO.WriteString('<td><pre>');
            IF edge_table.grid[y][x] <> 0 THEN
                TileSet.PrintTile(tile_set.tile[edge_table.grid[y][x]]);
            END;
            STextIO.WriteString('</pre></td>');
        END;
        STextIO.WriteString('</tr>');
    END;
    STextIO.WriteString('</table>');
    CheckGrid(edge_table, tile_set);
    STextIO.WriteString('</body></html>');
END PrintGrid;


PROCEDURE EdgeMatch(VAR tile_set : TileSet.TileSet);
    VAR edge_table  : EdgeTable;
    VAR edge_value  : EdgeValueList;
    VAR x, y        : TileSet.GridCoord;
    VAR i           : TileSet.TileIndex;
    VAR j           : EdgeIndex;
    VAR k           : EdgeValue;
BEGIN
    FOR y := MIN(TileSet.GridCoord) TO MAX(TileSet.GridCoord) DO
        FOR x := MIN(TileSet.GridCoord) TO MAX(TileSet.GridCoord) DO
            edge_table.grid[y][x] := 0;
        END;
    END;
    FOR k := 0 TO MaxEdgeValue DO
        edge_table.match[k] := NIL;
    END;
    FOR i := 1 TO tile_set.max_index DO
        edge_value := ComputeEdges(tile_set.tile[i]);
        FOR j := 1 TO Edges DO
            Push(edge_table.match[edge_value[j]], i);
        END;
    END;
    FindFirstMatch(edge_table, tile_set);
    PrintGrid(edge_table, tile_set);
END EdgeMatch;

END EdgeMatch.


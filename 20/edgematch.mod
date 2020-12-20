IMPLEMENTATION MODULE EdgeMatch;

FROM Storage IMPORT ALLOCATE;
FROM SYSTEM IMPORT TSIZE;
IMPORT TileSet;

PROCEDURE Push(VAR match : MatchListPtr;
               tile      : TileSet.TileIndex;
               edge      : TileSet.EdgeIndex);
    VAR item : MatchListPtr;
BEGIN
    ALLOCATE(item, TSIZE(MatchListItem));
    item^.next := match;
    item^.tile := tile;
    item^.edge := edge;
    match := item;
END Push;

PROCEDURE ComputeEdgeTable(VAR tile_set   : TileSet.TileSet;
                           VAR edge_table : EdgeTable);
    VAR i   : TileSet.TileIndex;
    VAR j   : TileSet.EdgeIndex;
    VAR k   : TileSet.EdgeValue;
BEGIN
    FOR k := 1 TO TileSet.MaxEdgeValue DO
        edge_table.match[k] := NIL;
    END;
    FOR i := 1 TO tile_set.max_index DO
        FOR j := 1 TO TileSet.Edges DO
            Push(edge_table.match[tile_set.tile[i].edge[j]], i, j);
        END;
    END;
END ComputeEdgeTable;


END EdgeMatch.


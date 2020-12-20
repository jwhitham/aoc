MODULE Hello;
IMPORT InOut;
IMPORT TileSet;
IMPORT EdgeMatch;

VAR tile_set : TileSet.TileSet;
VAR error    : BOOLEAN;
VAR edge_table : EdgeMatch.EdgeTable;

BEGIN
    TileSet.ReadTileSet("example_input", tile_set, error);
    IF error THEN
        RETURN;
    END;
    TileSet.ComputeEdges(tile_set);
    EdgeMatch.ComputeEdgeTable(tile_set, edge_table);
    InOut.WriteString('Hello world!');
    InOut.WriteLn;
    TileSet.PrintTile(TileSet.Rotate(tile_set.tile[1]));
END Hello.

MODULE Hello;
IMPORT TileSet;
IMPORT EdgeMatch;

VAR tile_set : TileSet.TileSet;
VAR error    : BOOLEAN;

BEGIN
    TileSet.ReadTileSet("example_input", tile_set, error);
    IF error THEN
        RETURN;
    END;
    EdgeMatch.EdgeMatch(tile_set);
    (* TileSet.PrintTile(TileSet.Rotate(tile_set.tile[1]));*)
END Hello.

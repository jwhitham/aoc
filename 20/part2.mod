MODULE Part2;
IMPORT TileSet;
IMPORT EdgeMatch;
IMPORT Monsters;
IMPORT STextIO;

VAR tile_set : TileSet.TileSet;
VAR grid     : EdgeMatch.Grid;
VAR error    : BOOLEAN;
VAR image    : Monsters.Image;

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
    Monsters.CreateImage(tile_set, grid, image);
    Monsters.Flip(image);
    Monsters.Rotate(image);
    Monsters.Rotate(image);
    Monsters.PrintImage(image);
END Part2.

MODULE Part2;
IMPORT TileSet;
IMPORT EdgeMatch;
IMPORT Monsters;
IMPORT STextIO;
IMPORT SWholeIO;

VAR tile_set : TileSet.TileSet;
VAR grid     : EdgeMatch.Grid;
VAR error    : BOOLEAN;
VAR image    : Monsters.Image;
VAR count    : CARDINAL;

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
    Monsters.CreateImage(tile_set, grid, image);
    Monsters.Flip(image);
    Monsters.Rotate(image);
    Monsters.Rotate(image);

    count := Monsters.FindMonsters(image);
    Monsters.PrintImage(image);

    STextIO.WriteString("number of monsters ");
    SWholeIO.WriteCard(count, 1);

    count := Monsters.CountWaves(image);
    STextIO.WriteString(" and roughness of sea ");
    SWholeIO.WriteCard(count, 1);
    STextIO.WriteLn;
END Part2.

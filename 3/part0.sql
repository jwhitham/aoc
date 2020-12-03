
CREATE TABLE input (y INTEGER NOT NULL, row TEXT, PRIMARY KEY (y));
INSERT INTO input (row) VALUES ("..##.......");
INSERT INTO input (row) VALUES ("#...#...#..");
INSERT INTO input (row) VALUES (".#....#..#.");
INSERT INTO input (row) VALUES ("..#.#...#.#");
INSERT INTO input (row) VALUES (".#...##..#.");
INSERT INTO input (row) VALUES ("..#.##.....");
INSERT INTO input (row) VALUES (".#.#.#....#");
INSERT INTO input (row) VALUES (".#........#");
INSERT INTO input (row) VALUES ("#.##...#...");
INSERT INTO input (row) VALUES ("#...##....#");
INSERT INTO input (row) VALUES (".#..#...#.#");

CREATE TABLE path1 (x INTEGER, y INTEGER);
INSERT INTO path1 (x, y)
    SELECT (((i1.y - 1) * 3) % LENGTH(i1.row)) + 1 AS x,
            i1.y AS y FROM input i1;

CREATE TABLE path2 (x INTEGER, y INTEGER, tree BOOLEAN);
INSERT INTO path2 (x, y, tree)
    SELECT p1.x, p1.y, (SUBSTR(i1.row, p1.x, 1) = '#')
        FROM input i1
        INNER JOIN path1 p1 ON i1.y = p1.y;

SELECT SUM(tree) FROM path2;

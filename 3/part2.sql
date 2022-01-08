
CREATE TABLE raw_input (row TEXT);
.import input raw_input

CREATE TABLE input (y INTEGER NOT NULL, row TEXT, PRIMARY KEY(y));
INSERT INTO input (row) SELECT row FROM raw_input;


CREATE TABLE vector (dx INTEGER, dy INTEGER);
INSERT INTO vector (dx, dy) VALUES (1, 1);
INSERT INTO vector (dx, dy) VALUES (3, 1);
INSERT INTO vector (dx, dy) VALUES (5, 1);
INSERT INTO vector (dx, dy) VALUES (7, 1);
INSERT INTO vector (dx, dy) VALUES (1, 2);

CREATE TABLE path0 (dx INTEGER, dy INTEGER, y INTEGER);
INSERT INTO path0 (dx, dy, y)
        SELECT v.dx, v.dy, ((i1.y - 1) * v.dy) + 1 FROM input i1
        INNER JOIN vector v;

CREATE TABLE path1 (dx INTEGER, dy INTEGER, x INTEGER, y INTEGER);
INSERT INTO path1 (dx, dy, x, y)
    SELECT p0.dx, p0.dy, (((p0.y - 1) / p0.dy) * p0.dx) + 1, p0.y FROM path0 p0;

CREATE TABLE path2 (dx INTEGER, dy INTEGER, x INTEGER, y INTEGER, tree BOOLEAN);
INSERT INTO path2 (dx, dy, x, y, tree)
    SELECT p1.dx, p1.dy, p1.x, p1.y,
            (SUBSTR(i1.row, ((p1.x - 1) % LENGTH(i1.row)) + 1, 1) = '#')
                FROM path1 p1 INNER JOIN input i1 ON i1.y = p1.y;

CREATE TABLE result (i INTEGER NOT NULL, dx INTEGER, dy INTEGER,
                     total INTEGER, PRIMARY KEY(i));
INSERT INTO result (dx, dy, total)
    SELECT dx, dy, SUM(tree) FROM path2 GROUP BY dx, dy;

/* Ah. There is SUM() but not PRODUCT(). */
CREATE TABLE product_out (cmd TEXT);
.output product_out.txt
.separator ""
SELECT "INSERT INTO product (total) SELECT 1";
SELECT " * ", total FROM result;
SELECT ";";
.output

CREATE TABLE product (total INTEGER);
.read product_out.txt
SELECT * FROM product;

    

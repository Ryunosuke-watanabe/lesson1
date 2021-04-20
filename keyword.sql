DROP TABLE IF EXISTS keyword;
CREATE TABLE keyword (
word text,
blue integer,
green integer,
red integer
);
INSERT INTO keyword (word, blue, green, red)
VALUES ('hot', 1, 1, 255);
INSERT INTO keyword (word, blue, green, red)
VALUES ('cool', 255, 1, 1);
INSERT INTO keyword (word, blue, green, red)
VALUES ('natural', 1, 255, 1);

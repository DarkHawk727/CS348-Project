INSERT INTO language SELECT * FROM read_csv('data/language.csv');
INSERT INTO film SELECT * FROM read_csv('data/film.csv');
INSERT INTO actor SELECT * FROM read_csv('data/actor.csv');
INSERT INTO category SELECT * FROM read_csv('data/category.csv');
INSERT INTO film_actor SELECT * FROM read_csv('data/film_actor.csv');
INSERT INTO film_category SELECT * FROM read_csv('data/film_category.csv');

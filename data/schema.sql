-- Create table for LANGUAGE
CREATE TABLE LANGUAGE (
    language_id SMALLINT PRIMARY KEY,
    name CHAR(50) NOT NULL
);

-- Create table for ACTOR
CREATE TABLE ACTOR (
    actor_id SMALLINT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL
);

-- Create indexes for ACTOR since we filter by first_name and last_name
CREATE INDEX idx_actor_first_name_upper ON ACTOR (UPPER(first_name));
CREATE INDEX idx_actor_last_name_upper ON ACTOR (UPPER(last_name));

-- Create table for CATEGORY
CREATE TABLE CATEGORY (
    category_id TINYINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create table for USER
CREATE TABLE USER (
    user_id TINYINT PRIMARY KEY,
    username VARCHAR(255) NOT NULL
);

-- Create table for FILM
CREATE TABLE FILM (
    film_id SMALLINT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    release_year INT,
    language_id SMALLINT,
    length INT,
    age_rating VARCHAR(10),
    FOREIGN KEY (language_id)
    REFERENCES LANGUAGE(language_id),
);

-- Create index for FILM since we filter by title
CREATE INDEX idx_film_title_upper ON FILM (UPPER(title));

-- Create table for FILM_ACTOR (junction table between ACTOR and FILM)
CREATE TABLE FILM_ACTOR (
    actor_id SMALLINT,
    film_id SMALLINT,
    PRIMARY KEY (actor_id, film_id),
    CONSTRAINT fk_film_actor_actor
        FOREIGN KEY (actor_id)
        REFERENCES ACTOR(actor_id),
    CONSTRAINT fk_film_actor_film
        FOREIGN KEY (film_id)
        REFERENCES FILM(film_id)
);

-- Create table for FILM_CATEGORY (junction table between FILM and CATEGORY)
CREATE TABLE FILM_CATEGORY (
    film_id SMALLINT,
    category_id TINYINT,
    PRIMARY KEY (film_id, category_id),
    CONSTRAINT fk_film_category_film
        FOREIGN KEY (film_id)
        REFERENCES FILM(film_id),
    CONSTRAINT fk_film_category_category
        FOREIGN KEY (category_id)
        REFERENCES CATEGORY(category_id)
);

-- Create table for RATINGS
CREATE TABLE RATINGS (
    user_id TINYINT,
    film_id SMALLINT,
    rating TINYINT NOT NULL,
    comment VARCHAR(255),
    PRIMARY KEY (user_id, film_id),
    CONSTRAINT fk_ratings_user
        FOREIGN KEY (user_id)
        REFERENCES USER(user_id),
    CONSTRAINT fk_ratings_film
        FOREIGN KEY (film_id)
        REFERENCES FILM(film_id)
);

-- Create Film Explorer View
CREATE VIEW FilmExplorerView AS
SELECT 
    f.film_id,
    f.title,
    f.release_year,
    f.length,
    f.age_rating,
    f.description,
    l.name AS language,
    GROUP_CONCAT(DISTINCT c.name ORDER BY c.name) AS categories,
    GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name) ORDER BY a.first_name, a.last_name) AS actors
FROM FILM f
LEFT JOIN LANGUAGE l ON f.language_id = l.language_id
LEFT JOIN FILM_CATEGORY fc ON f.film_id = fc.film_id
LEFT JOIN CATEGORY c ON fc.category_id = c.category_id
LEFT JOIN FILM_ACTOR fa ON f.film_id = fa.film_id
LEFT JOIN ACTOR a ON fa.actor_id = a.actor_id
GROUP BY f.film_id, f.title, f.release_year, f.length, f.age_rating, f.description, l.name;


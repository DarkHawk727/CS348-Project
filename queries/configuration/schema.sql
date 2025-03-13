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

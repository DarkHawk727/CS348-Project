SELECT FILM.title, 
FILM.description,
FILM.release_year,
FILM.age_rating, 
FILM.length,  
LANGUAGE.name, from FILM
INNER JOIN LANGUAGE ON FILM.language_id = LANGAUGE.language_id
where FILM.title like "%{user input}%";

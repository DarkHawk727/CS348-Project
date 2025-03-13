SELECT FILM.title, 
FILM.description,
FILM.release_year,
FILM.age_rating, 
FILM.length,  
LANGUAGE.name, from FILM
INNER JOIN LANGUAGE ON FILM.language_id = LANGUAGE.language_id
where FILM.title like '%A%';

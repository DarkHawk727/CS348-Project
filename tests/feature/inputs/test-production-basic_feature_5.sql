-- this is a basic recommendation query that returns all movies that have at least one actor shared  
-- and same category as user input query

WITH FilmActors AS (
    SELECT fa.actor_id
    FROM FILM_ACTOR fa
    WHERE fa.film_id = 73 -- user input for the id (will be passed from the Python API)
),
FilmCategories AS (
    SELECT fc.category_id
    FROM FILM_CATEGORY fc
    WHERE fc.film_id = 73 -- user input for the id (will be passed from the Python API)
)
SELECT DISTINCT f.film_id, f.title
FROM FILM f
JOIN FILM_ACTOR fa ON f.film_id = fa.film_id
JOIN FILM_CATEGORY fc ON f.film_id = fc.film_id
WHERE 
    fa.actor_id IN (SELECT actor_id FROM FilmActors) 
    OR fc.category_id IN (SELECT category_id FROM FilmCategories);



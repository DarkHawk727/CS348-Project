WITH FilmActors AS (
    SELECT fa.actor_id
    FROM FILM_ACTOR fa
    WHERE fa.film_id = {film_id}
),
FilmCategories AS (
    SELECT fc.category_id
    FROM FILM_CATEGORY fc
    WHERE fc.film_id = {film_id}
)
SELECT DISTINCT f.film_id, f.title, f.release_year, f.age_rating
FROM FILM f
JOIN FILM_ACTOR fa ON f.film_id = fa.film_id
JOIN FILM_CATEGORY fc ON f.film_id = fc.film_id
WHERE 
    f.film_id != {film_id}
    AND ({filter_condition})
ORDER BY f.title
LIMIT {limit}; 
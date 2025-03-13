WITH actor_count AS (
    SELECT COUNT(*) AS count FROM ACTOR
),
film_count AS (
    SELECT COUNT(*) AS count FROM FILM
)
SELECT actor_count.count AS actor_count, film_count.count AS film_count
FROM actor_count, film_count;

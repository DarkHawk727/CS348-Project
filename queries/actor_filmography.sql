SELECT f.title, f.release_year
FROM FILM f
JOIN FILM_ACTOR fa ON f.film_id = fa.film_id
JOIN ACTOR a ON fa.actor_id = a.actor_id
WHERE a.first_name = '{first_name}' AND a.last_name = '{last_name}'
ORDER BY f.release_year DESC

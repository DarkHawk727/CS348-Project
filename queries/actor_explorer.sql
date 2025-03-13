SELECT a.actor_id, a.first_name, a.last_name, COUNT(fa.film_id) as film_count
FROM ACTOR a
LEFT JOIN FILM_ACTOR fa ON a.actor_id = fa.actor_id
{filter}
GROUP BY a.actor_id, a.first_name, a.last_name
ORDER BY a.last_name, a.first_name

SELECT f.title, AVG(r.rating) AS average_rating
FROM FILM AS f
JOIN RATINGS AS r ON f.film_id = r.film_id
GROUP BY f.film_id, f.title;

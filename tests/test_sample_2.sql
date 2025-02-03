SELECT f.title
FROM film AS f
JOIN language AS l ON f.language_id=l.language_id
WHERE l.name="English";

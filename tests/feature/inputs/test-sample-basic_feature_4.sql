 SELECT f.*, l.name as language
            FROM FILM f
            LEFT JOIN LANGUAGE l ON f.language_id = l.language_id
            WHERE f.title = 'ACADEMY DINOSAUR'

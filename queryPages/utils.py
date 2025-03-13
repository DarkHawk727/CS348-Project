# general query for attributes
def get_all_languages(conn):
    return conn.execute("SELECT language_id, name FROM LANGUAGE ORDER BY name").fetchdf()

def get_all_categories(conn):
    return conn.execute("SELECT category_id, name FROM CATEGORY ORDER BY name").fetchdf()

def get_film_release_range(conn):
    return conn.execute("SELECT MIN(release_year), MAX(release_year) FROM FILM").fetchone()

# Filter Query String
def apply_filters(query, conn):
    return conn.execute(query).fetchdf()

# Instance queries
def get_film_details(conn, film_title):
    return conn.execute(f"""
            SELECT f.*, l.name as language
            FROM FILM f
            LEFT JOIN LANGUAGE l ON f.language_id = l.language_id
            WHERE f.title = '{film_title}'
        """).fetchdf()

def get_film_actors(conn, film_id):
    conn.execute(f"""
                    SELECT a.first_name, a.last_name
                    FROM ACTOR a
                    JOIN FILM_ACTOR fa ON a.actor_id = fa.actor_id
                    WHERE fa.film_id = {film_id}
                """).fetchdf()

def get_film_categories(conn, film_id):
    conn.execute(f"""
                    SELECT c.name
                    FROM CATEGORY c
                    JOIN FILM_CATEGORY fc ON c.category_id = fc.category_id
                    WHERE fc.film_id = {film_id}
                """).fetchdf()


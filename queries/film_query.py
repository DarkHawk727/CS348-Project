def get_film_release_range(conn):
    return conn.execute("SELECT MIN(release_year), MAX(release_year) FROM FILM").fetchone()

# Filter Query String
def apply_film_filters(query,params, conn):
    return conn.execute(query, params).fetchdf()

# Instance queries
def get_film_details(conn, film_title):
    return conn.execute(f"""
            SELECT f.*
            FROM FilmExplorerView f
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


# general query for attributes or DB structure
def get_all_languages(conn):
    return conn.execute("SELECT language_id, name FROM LANGUAGE ORDER BY name").fetchdf()

def get_all_categories(conn):
    return conn.execute("SELECT category_id, name FROM CATEGORY ORDER BY name").fetchdf()

def get_all_table_info(conn):
    return conn.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'main'
        """).fetchdf()

def get_all_table_columns(conn, table_name):
    return conn.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table_name}' AND table_schema = 'main'
            """).fetchdf()
        
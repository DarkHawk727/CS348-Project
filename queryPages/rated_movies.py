import streamlit as st
import pandas as pd
from queries.film_query import *
from queries.general_query import *

# todo move the queries away from here and into the queries folder (should split up the queries folder into different files for each page)
def show(conn):
    st.header("Top Rated Movies")
    
    # general filters subsection -----
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        # Get all categories
        categories = get_all_categories(conn)
        selected_category = st.selectbox("Filter by Category", ["All"] + categories["name"].tolist())
    
    with col2:
        # Get all languages
        languages = get_all_languages(conn)
        selected_language = st.selectbox("Filter by Language", ["All"] + languages["name"].tolist())
    
    # Build query based on filters (not happy with this still being in the file)
    query = """
SET disabled_optimizers = 'join_order,build_side_probe_side';
SELECT f.title, AVG(r.rating) AS average_rating, COUNT(r.rating) AS review_count, l.name
FROM FILM AS f
JOIN LANGUAGE AS l ON l.language_id = f.language_id
JOIN RATINGS AS r ON f.film_id = r.film_id
    """
    
    where_clauses = []
    
    if selected_category != "All":
        query += " JOIN FILM_CATEGORY fc ON f.film_id = fc.film_id JOIN CATEGORY c ON fc.category_id = c.category_id "
        where_clauses.append(f"c.name = '{selected_category}'")
    
    if selected_language != "All":
        where_clauses.append(f"l.name = '{selected_language}'")
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += "GROUP BY f.film_id, f.title, l.name ORDER BY average_rating, review_count DESC;"
    
    films = apply_film_filters(query, conn)
    apply_film_filters("SET disabled_optimizers = '';", conn)
    
    st.dataframe(films)
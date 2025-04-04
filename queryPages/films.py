import streamlit as st
import pandas as pd
from queries.film_query import *
from queries.general_query import *

# todo move the queries away from here and into the queries folder (should split up the queries folder into different files for each page)
def show(conn):
    st.header("Film Explorer")
    
    # Film Name Input
    movie_name_string = st.text_input("Film Name Search",value="")
    # general filters subsection -----
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get all categories
        categories = get_all_categories(conn)
        selected_category = st.selectbox("Filter by Category", ["All"] + categories["name"].tolist())
    
    with col2:
        # Get all languages
        languages = get_all_languages(conn)
        selected_language = st.selectbox("Filter by Language", ["All"] + languages["name"].tolist())
    
    with col3: # there is something wrong with the actual movie data with all the movies being from 2005-2006 (need to update the data)
        # Year range
        min_year, max_year = get_film_release_range(conn)
        if min_year is None: min_year = 1900
        if max_year is None: max_year = 2023
        

        year_range = st.slider("Release Year", min_year-1, max_year+1, (min_year-1, max_year+1))
    
    query = """
        SELECT film_id, title, release_year, length, age_rating, language, categories
        FROM FilmExplorerView
        WHERE release_year BETWEEN ? AND ?
    """
    params = [year_range[0], year_range[1]]

    if selected_category != "All":
        query += " AND categories LIKE ?"
        params.append(f"%{selected_category}%")

    if selected_language != "All":
        query += " AND language = ?"
        params.append(selected_language)

    if movie_name_string:
        query += " AND UPPER(title) LIKE ?"
        params.append(f"%{movie_name_string.upper()}%")

    query += " ORDER BY title"

    films = apply_film_filters(query,conn, params)
    st.dataframe(films)
    
    # Film details subsection -----
    if not films.empty:
        st.subheader("Film Details")
        selected_film_title = st.selectbox("Select a film for details", films["title"].tolist())
        
        film_details = get_film_details(conn, selected_film_title)
        
        if not film_details.empty:
            film_id = film_details.iloc[0]["film_id"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Title:**", film_details.iloc[0]["title"])
                st.write("**Release Year:**", film_details.iloc[0]["release_year"])
                st.write("**Language:**", film_details.iloc[0]["language"])
                st.write("**Length:**", film_details.iloc[0]["length"], "minutes")
                st.write("**Age Rating:**", film_details.iloc[0]["age_rating"])
                st.write("**Description:**", film_details.iloc[0]["description"])
            
            with col2:
                # Get actors for this film
                actors = get_film_actors(conn, film_id)
                
                st.write("**Actors:**")
                if actors:
                    for _, actor in actors.iterrows():
                        st.write(f"- {actor['first_name']} {actor['last_name']}")
                else:
                    st.write("No actors listed")
                
                # Get categories for this film
                categories = get_film_categories(conn, film_id)
                
                st.write("**Categories:**")
                if categories:
                    for _, category in categories.iterrows():
                        st.write(f"- {category['name']}")
                else:
                    st.write("No categories listed") 
    
    # same with actors, need to add more advanced features like most famous actors in a film, most popular film of a category, some stuff with reviews etc.
import streamlit as st
import pandas as pd
import os

def load_query(filename):
    path = os.path.join("queries", filename)
    with open(path, "r") as file:
        return file.read()


'''
This function sets up the recommendation page
will return all movies that are similar to the selected film

the similarity parameters are one of the following:
- actors
- categories (genres)


still need to decide if we want more advanced features to this or its ok (lmk)
'''

def show(conn):
    st.header("Movie Recommendations")
    st.markdown(
        "Find movies similar to your favorites based on either actors or categories."
    )
    
    films = conn.execute("SELECT film_id, title FROM FILM ORDER BY title").fetchdf()
    selected_film = st.selectbox("Select a film you enjoyed", films["title"].tolist())
    
    film_id = conn.execute(f"SELECT film_id FROM FILM WHERE title = '{selected_film}'").fetchone()[0]
    
    # Recommendation options - radio button for either actor or category
    recommendation_type = st.radio(
        "Recommend movies by:",
        ["Actor", "Category (Genre)"]
    )
    
    max_recommendations = st.slider("Max Recommendations", 5, 30, 10)
    
    # Build and execute recommendation query
    if st.button("Get Recommendations"):
        query_template = load_query("movie_recommendations.sql")
        
        if recommendation_type == "Actor":
            filter_condition = "fa.actor_id IN (SELECT actor_id FROM FilmActors)"
        else: 
            filter_condition = "fc.category_id IN (SELECT category_id FROM FilmCategories)"
    
    
        query = query_template.format(
            film_id=film_id,
            filter_condition=filter_condition,
            limit=max_recommendations
        )
        
        # Execute query
        recommendations = conn.execute(query).fetchdf()
        
        if recommendations.empty:
            st.info(f"No recommendations found based on {recommendation_type}.")
        else:
            st.subheader(f"Recommended Movies Similar to '{selected_film}' by {recommendation_type}")
            st.dataframe(recommendations) 
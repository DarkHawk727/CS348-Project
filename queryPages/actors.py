import streamlit as st
import pandas as pd
from queries.actor_query import *

'''
Will need to import the actual queries from queries folder todo
'''
def show(conn):
    st.header("Actor Explorer")
    
    # Search by name subsection -----
    search_term = st.text_input("Search actors by name")
    
    query = """
        SELECT a.actor_id, a.first_name, a.last_name, COUNT(fa.film_id) as film_count
        FROM ACTOR a
        LEFT JOIN FILM_ACTOR fa ON a.actor_id = fa.actor_id
    """

    if search_term:
        query += f" WHERE a.first_name ILIKE '%{search_term}%' OR a.last_name ILIKE '%{search_term}%'"
    
    query += " GROUP BY a.actor_id, a.first_name, a.last_name ORDER BY a.last_name, a.first_name"
    
    actors = conn.execute(query).fetchdf()
    st.dataframe(actors)
    
    # Actor details subsection -----
    if not actors.empty:
        st.subheader("Actor Filmography")
        
        # Create a list of actor names
        actor_options = [f"{row['first_name']} {row['last_name']}" for _, row in actors.iterrows()]
        selected_actor = st.selectbox("Select an actor", actor_options)
        
        first_name, last_name = selected_actor.split(" ", 1)
        
        # Get films for this actor
        films = get_actor_films(conn, first_name, last_name)
        
        st.write(f"**Films with {selected_actor}:**")
        st.dataframe(films) 
    
        # TODO: Add more advanced features here like related actors, shared movies between actors, etc.

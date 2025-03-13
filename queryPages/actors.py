import os

import pandas as pd
import streamlit as st



def load_query(filename):
    """Load an SQL query from a file in the 'queries' folder."""
    path = os.path.join("queries", filename)
    with open(path, "r") as file:
        return file.read()


def show(conn):
    st.header("Actor Explorer")
    st.markdown(
        "Only remember the first or last name of an actor? No worries! With this handy tool, you can find all actors that have names similar to the one you provide."
    )

    # --- Search by name subsection ---
    search_term = st.text_input(
        "Enter first OR last name", help="You can also include a part of either name"
    )

    # Load the base actor query template
    actor_query_template = load_query("actor_explorer.sql")

    # Prepare filter clause if search_term is provided
    filter_clause = ""
    if search_term:
        filter_clause = f"WHERE a.first_name ILIKE '%{search_term}%' OR a.last_name ILIKE '%{search_term}%'"

    # Inject the filter into the query template
    actor_query = actor_query_template.format(filter=filter_clause)

    actors = conn.execute(actor_query).fetchdf()
    st.dataframe(actors)

    # --- Actor details subsection ---
    if not actors.empty:
        st.subheader("Actor Filmography")
        actor_options = [
            f"{row['first_name']} {row['last_name']}" for _, row in actors.iterrows()
        ]
        selected_actor = st.selectbox("Select an actor", actor_options)
        first_name, last_name = selected_actor.split(" ", 1)

        # Load and format the filmography query
        filmography_query_template = load_query("actor_filmography.sql")
        filmography_query = filmography_query_template.format(
            first_name=first_name, last_name=last_name
        )

        films = conn.execute(filmography_query).fetchdf()

        st.write(f"**Films with {selected_actor}:**")
        st.dataframe(films)

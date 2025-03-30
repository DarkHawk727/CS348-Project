import importlib
import os

import duckdb
import pandas as pd
import streamlit as st

# Import pages (do not change name of folder since if its pages it will be displayed in the sidebar)
from queryPages import (
    actors,
    custom_query,
    films,
    rated_movies,
    recommendations,
    schema_viewer,
)

# Set up page configuration
st.set_page_config(
    page_title="Movie Database Explorer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",  # change to "collapsed" if you want to hide the sidebar
)


# Initialize database connection (taken from duckdb recommeded practices)
@st.cache_resource
def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")

    conn = duckdb.connect("data/movies.db")

    # Check if tables already exist (bug came up if I ran this a bunch of times)
    table_count = conn.execute(
        """
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_schema = 'main' AND table_name = 'FILM'
    """
    ).fetchone()[0]

    # Initialize schema only if tables don't exist
    if table_count == 0:
        with open("data/schema.sql", "r") as f:
            schema_sql = f.read()
            conn.execute(schema_sql)

    # not sure if this section is needed but better safe than sorry
    # Check if data exists
    film_count = conn.execute("SELECT COUNT(*) FROM FILM").fetchone()[0]

    # Load data from CSV files if tables are empty (find better way to do this)
    if film_count == 0:
        try:
            with open("data/data.sql", "r") as f:
                data_sql = f.read()
                conn.execute(data_sql)
            st.sidebar.success("Data loaded successfully from CSV files!")
        except Exception as e:
            st.sidebar.error(f"Error loading data: {e}")
            st.sidebar.info(
                "Please ensure your CSV files exist in the data/ directory."
            )

    return conn


# Get database connection
conn = init_db()

# Sidebar for navigation
st.sidebar.title("Movie Database Explorer")
st.sidebar.markdown("---")

# Navigation
st.sidebar.subheader("Navigation")
page = st.sidebar.radio(
    "Select a page",
    [
        "Films",
        "Actors",
        "Top Rated",
        "Recommendations",
        "Schema Viewer",
        "Custom Query",
    ],
    label_visibility="collapsed",  # something here stops default pages from being displayed donot remove
)

# Database info in sidebar (add more later)
st.sidebar.markdown("---")
st.sidebar.subheader("Database Info")
film_count = conn.execute("SELECT COUNT(*) FROM FILM").fetchone()[0]
actor_count = conn.execute("SELECT COUNT(*) FROM ACTOR").fetchone()[0]

st.sidebar.markdown(f"**Films:** {film_count}")
st.sidebar.markdown(f"**Actors:** {actor_count}")

# Main content
st.title(f"Movie Database - {page}")

# Display the selected page
if page == "Films":
    films.show(conn)
elif page == "Actors":
    actors.show(conn)
elif page == "Top Rated":
    rated_movies.show(conn)
elif page == "Recommendations":
    recommendations.show(conn)
elif page == "Schema Viewer":
    schema_viewer.show(conn)
elif page == "Custom Query":
    custom_query.show(conn)

# CSS for the app, feel free to change this was a default option
st.markdown(
    """
<style>
    .stDataFrame {
        margin-top: 20px;
        margin-bottom: 30px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""",
    unsafe_allow_html=True,
)

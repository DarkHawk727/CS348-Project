import duckdb
import streamlit as st
import pandas as pd
import os

# Set up page configuration
st.set_page_config(
    page_title="Movie Database Explorer",
    page_icon="🎬",
    layout="wide"
)

# Initialize database connection
@st.cache_resource
def init_db():
    # Create database directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Connect to DuckDB
    conn = duckdb.connect('data/movies.db')
    
    # Check if tables already exist
    table_count = conn.execute("""
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_schema = 'main' AND table_name = 'FILM'
    """).fetchone()[0]
    
    # Initialize schema only if tables don't exist
    if table_count == 0:
        with open('queries/schema.sql', 'r') as f:
            schema_sql = f.read()
            conn.execute(schema_sql)
    
    # Check if data exists
    film_count = conn.execute("SELECT COUNT(*) FROM FILM").fetchone()[0]
    
    # Load data from CSV files if tables are empty
    if film_count == 0:
        try:
            with open('queries/data.sql', 'r') as f:
                data_sql = f.read()
                conn.execute(data_sql)
            st.sidebar.success("Data loaded successfully from CSV files!")
        except Exception as e:
            st.sidebar.error(f"Error loading data: {e}")
            st.sidebar.info("Please ensure your CSV files exist in the data/ directory.")
    
    return conn

# Get database connection
conn = init_db()

# Sidebar for navigation
st.sidebar.title("Movie Database")
page = st.sidebar.selectbox("Choose a page", ["Films", "Actors", "Categories", "Ratings", "Run Custom Query"])

# Main content
st.title(f"Movie Database - {page}")

# Films page
if page == "Films":
    st.header("Film Explorer")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get all categories
        categories = conn.execute("SELECT category_id, name FROM CATEGORY ORDER BY name").fetchdf()
        selected_category = st.selectbox("Filter by Category", ["All"] + categories["name"].tolist())
    
    with col2:
        # Get all languages
        languages = conn.execute("SELECT language_id, name FROM LANGUAGE ORDER BY name").fetchdf()
        selected_language = st.selectbox("Filter by Language", ["All"] + languages["name"].tolist())
    
    with col3:
        # Year range
        min_year, max_year = conn.execute("SELECT MIN(release_year), MAX(release_year) FROM FILM").fetchone()
        if min_year is None: min_year = 1900
        if max_year is None: max_year = 2023
        
        # Handle case where min_year equals max_year
        if min_year == max_year:
            slider_min = min_year - 1
            slider_max = max_year + 1
            default_value = (min_year, max_year)
        else:
            slider_min = min_year
            slider_max = max_year
            default_value = (min_year, max_year)
        
        year_range = st.slider("Release Year", slider_min, slider_max, default_value)
    
    # Build query based on filters
    query = """
        SELECT f.film_id, f.title, f.release_year, f.length, f.age_rating, l.name as language
        FROM FILM f
        LEFT JOIN LANGUAGE l ON f.language_id = l.language_id
    """
    
    where_clauses = []
    where_clauses.append(f"f.release_year BETWEEN {year_range[0]} AND {year_range[1]}")
    
    if selected_category != "All":
        query += " JOIN FILM_CATEGORY fc ON f.film_id = fc.film_id JOIN CATEGORY c ON fc.category_id = c.category_id"
        where_clauses.append(f"c.name = '{selected_category}'")
    
    if selected_language != "All":
        where_clauses.append(f"l.name = '{selected_language}'")
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += " ORDER BY f.title"
    
    # Execute query and display results
    films = conn.execute(query).fetchdf()
    st.dataframe(films)
    
    # Film details
    if not films.empty:
        st.subheader("Film Details")
        selected_film_title = st.selectbox("Select a film for details", films["title"].tolist())
        
        film_details = conn.execute(f"""
            SELECT f.*, l.name as language
            FROM FILM f
            LEFT JOIN LANGUAGE l ON f.language_id = l.language_id
            WHERE f.title = '{selected_film_title}'
        """).fetchdf()
        
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
                actors = conn.execute(f"""
                    SELECT a.first_name, a.last_name
                    FROM ACTOR a
                    JOIN FILM_ACTOR fa ON a.actor_id = fa.actor_id
                    WHERE fa.film_id = {film_id}
                """).fetchdf()
                
                st.write("**Actors:**")
                if not actors.empty:
                    for _, actor in actors.iterrows():
                        st.write(f"- {actor['first_name']} {actor['last_name']}")
                else:
                    st.write("No actors listed")
                
                # Get categories for this film
                categories = conn.execute(f"""
                    SELECT c.name
                    FROM CATEGORY c
                    JOIN FILM_CATEGORY fc ON c.category_id = fc.category_id
                    WHERE fc.film_id = {film_id}
                """).fetchdf()
                
                st.write("**Categories:**")
                if not categories.empty:
                    for _, category in categories.iterrows():
                        st.write(f"- {category['name']}")
                else:
                    st.write("No categories listed")

# Actors page
elif page == "Actors":
    st.header("Actor Explorer")
    
    # Search by name
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
    
    # Actor details
    if not actors.empty:
        st.subheader("Actor Filmography")
        
        # Create a list of actor names
        actor_options = [f"{row['first_name']} {row['last_name']}" for _, row in actors.iterrows()]
        selected_actor = st.selectbox("Select an actor", actor_options)
        
        first_name, last_name = selected_actor.split(" ", 1)
        
        # Get films for this actor
        films = conn.execute(f"""
            SELECT f.title, f.release_year
            FROM FILM f
            JOIN FILM_ACTOR fa ON f.film_id = fa.film_id
            JOIN ACTOR a ON fa.actor_id = a.actor_id
            WHERE a.first_name = '{first_name}' AND a.last_name = '{last_name}'
            ORDER BY f.release_year DESC
        """).fetchdf()
        
        st.write(f"**Films with {selected_actor}:**")
        st.dataframe(films)

# Categories page
elif page == "Categories":
    st.header("Categories")
    
    # Get all categories with film counts
    categories = conn.execute("""
        SELECT c.category_id, c.name, COUNT(fc.film_id) as film_count
        FROM CATEGORY c
        LEFT JOIN FILM_CATEGORY fc ON c.category_id = fc.category_id
        GROUP BY c.category_id, c.name
        ORDER BY c.name
    """).fetchdf()
    
    st.dataframe(categories)
    
    # Category details
    if not categories.empty:
        st.subheader("Films by Category")
        selected_category = st.selectbox("Select a category", categories["name"].tolist())
        
        # Get films for this category
        films = conn.execute(f"""
            SELECT f.title, f.release_year, f.age_rating
            FROM FILM f
            JOIN FILM_CATEGORY fc ON f.film_id = fc.film_id
            JOIN CATEGORY c ON fc.category_id = c.category_id
            WHERE c.name = '{selected_category}'
            ORDER BY f.release_year DESC
        """).fetchdf()
        
        st.write(f"**Films in {selected_category} category:**")
        st.dataframe(films)

# Ratings page
elif page == "Ratings":
    st.header("Ratings")
    
    # Show average ratings by film
    avg_ratings = conn.execute("""
        SELECT f.title, AVG(r.rating) as avg_rating, COUNT(r.rating) as rating_count
        FROM FILM f
        JOIN RATINGS r ON f.film_id = r.film_id
        GROUP BY f.title
        ORDER BY avg_rating DESC
    """).fetchdf()
    
    st.subheader("Average Ratings by Film")
    st.dataframe(avg_ratings)
    
    # Show recent ratings with comments
    recent_ratings = conn.execute("""
        SELECT f.title, u.username, r.rating, r.comment
        FROM RATINGS r
        JOIN FILM f ON r.film_id = f.film_id
        JOIN USER u ON r.user_id = u.user_id
        WHERE r.comment IS NOT NULL
        ORDER BY r.rating DESC
        LIMIT 10
    """).fetchdf()
    
    st.subheader("Recent Ratings with Comments")
    st.dataframe(recent_ratings)

# Custom Query page
elif page == "Run Custom Query":
    st.header("Custom SQL Query")
    
    # Show table schema
    if st.checkbox("Show Database Schema"):
        tables = conn.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'main'
        """).fetchdf()
        
        for _, row in tables.iterrows():
            table = row['table_name']
            st.subheader(f"Table: {table}")
            columns = conn.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table}' AND table_schema = 'main'
            """).fetchdf()
            st.dataframe(columns)
    
    # Custom query input
    query = st.text_area("Enter your SQL query", height=150)
    
    if st.button("Run Query"):
        if query:
            try:
                result = conn.execute(query).fetchdf()
                st.dataframe(result)
            except Exception as e:
                st.error(f"Error executing query: {e}")
        else:
            st.warning("Please enter a query")

# Add some CSS to make it look nicer
st.markdown("""
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
""", unsafe_allow_html=True)


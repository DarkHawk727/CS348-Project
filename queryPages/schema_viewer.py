import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

def mermaid(code: str) -> None:
    components.html(
        f"""
        <div style="width: 100%; overflow: auto;">
            <pre class="mermaid" style="width: 100%;">
                {code}
            </pre>
        </div>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize();
        </script>
        """,
        height=600, 
    )

def show(conn):
    st.header("Database Schema Viewer")
    st.markdown(
        "View the structure of the movie database tables."
    )
    
    st.subheader("Database Entity Relationship Diagram")
    
    # from milestone 1
    mermaid_code = """
    erDiagram
        ACTOR {
            SMALLINT actor_id PK
            VARCHAR first_name
            VARCHAR last_name
        }
    
        FILM {
            SMALLINT film_id PK
            VARCHAR title
            TINYINT language_id FK
            TINYINT original_language_id FK
        }
    
        LANGUAGE {
            SMALLINT language_id PK
            CHAR name
        }
    
        CATEGORY {
            TINYINT category_id PK
            VARCHAR name
        }
    
        FILM_CATEGORY {
            SMALLINT film_id FK
            TINYINT category_id FK
        }
    
        FILM_ACTOR {
            SMALLINT actor_id FK
            SMALLINT film_id FK
        }
    
        USER {
            TINYINT user_id PK
            VARCHAR username
        }
    
        RATINGS {
            TINYINT user_id FK
            SMALLINT film_id FK
            TINYINT rating
            VARCHAR comment
        }

      ACTOR ||--o{ FILM_ACTOR : appears_in
      FILM ||--o{ FILM_ACTOR : has_actors
      FILM ||--o{ FILM_CATEGORY : categorized_by
      CATEGORY ||--o{ FILM_CATEGORY : includes_films
      LANGUAGE ||--o{ FILM : spoken_language
      LANGUAGE ||--o{ FILM : original_language
      FILM ||--o{ RATINGS : was_rated
      USER ||--o{ RATINGS : rated
    """
    
    mermaid(mermaid_code)
    
    st.subheader("Table Details")
    
    # Get all tables in the database
    tables = conn.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'main'
        ORDER BY table_name
    """).fetchdf()
    
    # Display all tables and their columns
    for table_name in tables["table_name"]:
        with st.expander(f"Table: {table_name}"):
            # using the information schema to get the columns and data types (works on duckdb and I think postgres)
            columns = conn.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table_name}' AND table_schema = 'main'
                ORDER BY ordinal_position
            """).fetchdf()
            
            # Display table columns
            st.dataframe(columns, hide_index=True)
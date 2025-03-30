import streamlit as st
import pandas as pd

def show(conn):
    st.header("Database Schema Viewer")
    st.markdown(
        "View the structure of the movie database tables."
    )
    
    tables = conn.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'main'
        ORDER BY table_name
    """).fetchdf()
    
    # Display all tables and their columns
    for table_name in tables["table_name"]:
        with st.expander(f"Table: {table_name}"):
            # using the information schema to get the columns and data types (works on dyckdb and I think postgres)
            columns = conn.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table_name}' AND table_schema = 'main'
                ORDER BY ordinal_position
            """).fetchdf()
            
            st.dataframe(columns, hide_index=True)

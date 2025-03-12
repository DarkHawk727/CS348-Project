import streamlit as st
import pandas as pd

'''
This page is for running custom queries on the database. need to import the actual queries from queries folder (or extract the placeholders I made here)
'''

def show(conn):
    st.header("Custom SQL Query")
    
    # Show table schema subsection -----
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
    
    # Custom query input subsection -----
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
    
    # I think that the personal queries are good enough as is -> only other feature I can think of is some way to visualize the graph with arrows and stuff (maybe?)
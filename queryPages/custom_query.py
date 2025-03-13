import streamlit as st
import pandas as pd
from queries.general_query import *

'''
This page is for running custom queries on the database. need to import the actual queries from queries folder (or extract the placeholders I made here)
'''
def show(conn):
    st.header("Custom SQL Query")
    
    # Show table schema subsection -----
    if st.checkbox("Show Database Schema"):
        tables = get_all_table_info(conn)
        for _, row in tables.iterrows():
            table = row['table_name']
            st.subheader(f"Table: {table}")
            columns = get_all_table_columns(conn, table)
            st.dataframe(columns)
    
    # Custom query input subsection -----
    query = st.text_area("Enter your SQL query", height=150)
    
    # need to find out a more efficient way to check for forbidden words, probably some library that can do it
    forbidden_words = ["DROP TABLE", "CREATE TABLE", "ALTER TABLE", "INSERT INTO", "UPDATE", "DELETE", "CREATE INDEX", "CREATE VIEW", "CREATE"]
    
    if st.button("Run Query"):    
    
        if query:
            try:
                if any(word in query.upper() for word in forbidden_words):
                    raise Exception("You cannot alter the database in this way")

                result = conn.execute(query).fetchdf()
                st.dataframe(result)
            except Exception as e:
                st.error(f"Error executing query: {e}")
        else:
            st.warning("Please enter a query") 
    
    # I think that the personal queries are good enough as is -> only other feature I can think of is some way to visuconn.execalize the graph with arrows and stuff (maybe?)
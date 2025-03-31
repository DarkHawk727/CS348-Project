import duckdb
import pandas as pd
import streamlit as st
from streamlit_ace import st_ace


def is_query_safe(query: str) -> bool:
    unsafe_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "CREATE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "REPLACE",
        "MERGE",
    ]

    query_upper = query.upper()

    for keyword in unsafe_keywords:
        if keyword in query_upper:
            return False
    return True


# Example usage:
user_query = st.text_area("Enter your SQL query:")
if user_query:
    if is_query_safe(user_query):
        st.info("Query is safe to run.")
        # Run the query...
    else:
        st.error(
            "The query contains potential modification commands and was blocked for safety."
        )


def show(conn):
    st.markdown(
        "If you aren't satisfied with the current selection of queries, you can try writing your own."
    )
    st.warning(
        "For safety, the connection to the database is in read-only. You will not be able to modify the contents.",
        icon="⚠️",
    )
    st.info(
        "Pro-Tip: You can check out the Schema Viewer page to know how to structure your queries!",
        icon="ℹ️",
    )
    st.header("Custom SQL Query")

    content = st_ace(
        placeholder="Write your SQL query here...",
        language="sql",
        theme="monokai",
        key="custom_query_editor",  # Provide a unique key here
        keybinding="vscode",
        font_size=14,
        tab_size=4,
        wrap=True,
        auto_update=False,
        readonly=False,
    )

    if content:
        if is_query_safe(content):
            st.info("Query is safe to run.")
            result = conn.execute(content).fetchdf()
            st.dataframe(result)
        else:
            st.error(
                "The query contains potential modification commands and was blocked for safety."
            )

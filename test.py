import duckdb

# Create database schema
with open("queries/schema.sql", "r") as file:
    lines = "".join(file.readlines())
duckdb.sql(lines)

# Insert data into tables
with open("queries/data.sql", "r") as file:
    lines = "".join(file.readlines())
duckdb.sql(lines)

duckdb.sql("""
SELECT * FROM film;
""").show()

# # Show all the tables and verify that there are 1000 rows.
# with open("queries/check.sql", "r") as file:
#     lines = "".join(file.readlines())
# duckdb.sql(lines)
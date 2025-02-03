import duckdb

if __name__ == "__main__":
    # Create database schema
    with open("queries/schema.sql", "r") as file:
        lines = "".join(file.readlines())
    duckdb.sql(lines)

    # Insert data into tables
    with open("queries/data.sql", "r") as file:
        lines = "".join(file.readlines())
    duckdb.sql(lines)

    for i in range(1, 5):
        with open(f"tests/basic_feature{i}.sql", "r") as file:
            lines = "".join(file.readlines())
        duckdb.sql(lines).show()

import sys
import os
import duckdb

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    # Run schema
    with open("queries/schema.sql", "r", encoding="utf-8") as file:
        schema_sql = file.read()
    duckdb.sql(schema_sql)

    # Run data
    with open("queries/data.sql", "r", encoding="utf-8") as file:
        data_sql = file.read()
    duckdb.sql(data_sql)

    # Ensure the outputs directory exists
    os.makedirs("outputs", exist_ok=True)

    # List of test files to run
    test_files = [
        "tests/basic_feature_1.sql",
        "tests/basic_feature_2.sql",
        "tests/basic_feature_4.sql"
    ]

    for test_file in test_files:
        with open(test_file, "r", encoding="utf-8") as file:
            sql_query = file.read()
        result = duckdb.sql(sql_query)
        # Show results in the console
        result.show()
        # Convert result to a DataFrame, then to a string
        output_str = result.fetchdf().to_string(index=False)
        # Write the output to a corresponding file in the outputs directory
        output_file = os.path.join("outputs", os.path.basename(test_file).replace(".sql", ".out"))
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(output_str)

import sys
import duckdb

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    with open("queries/schema.sql", "r", encoding="utf-8") as file:
        lines = "".join(file.readlines())
    duckdb.sql(lines)

    with open("queries/data.sql", "r", encoding="utf-8") as file:
        lines = "".join(file.readlines())
    duckdb.sql(lines)

    ### add your tests here

    with open(f"tests/basic_feature_4.sql", "r", encoding="utf-8") as file:
        lines = "".join(file.readlines())
    duckdb.sql(lines).show()

import duckdb

# Connect to your DuckDB database file
con = duckdb.connect('hubspot.duckdb')

# Execute a query to list all tables
# tables = con.execute("SELECT table_name FROM information_schema.tables").fetchall()
#
# # Print the list of tables
# for table in tables:
#     print(table)
#
#
tables = con.execute("SELECT * from hubspot_dataset.companies").fetchall()

for table in tables:
    print(table)
import duckdb

con = duckdb.connect("items.duckdb")

con.execute("""
    COPY items FROM 'items.csv' (HEADER, DELIMITER ',')
""")

result = con.execute("SELECT * FROM items").fetchall()
print(result)
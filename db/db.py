import duckdb

con = duckdb.connect("test.db",read_only=True)
print("terminal 1 hold the log")
input()
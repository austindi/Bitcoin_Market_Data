import duckdb

conn = duckdb.connect("database/bitcoin.db")

print("Available tables:", conn.execute("SHOW TABLES").fetchall())

df = conn.execute("SELECT * FROM crypto_data").df()

print(df)

conn.close()

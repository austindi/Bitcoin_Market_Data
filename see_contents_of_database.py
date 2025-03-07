import duckdb

con = duckdb.connect( "database/bitcoin.db" ) 

print( "Available tables:", conn.execute("SHOW TABLES").fetchall())

df - con.execute( "SELECT * FROM crypto_data" ).df() 

print( df ) 
con.close() 

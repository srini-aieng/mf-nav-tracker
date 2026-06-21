import sqlite3

conn = sqlite3.connect("data/nav.db")

with open("schema.sql", "r") as sql_file:
    schema = sql_file.read()

conn.executescript(schema)

conn.commit()
conn.close()

print("Database initialized successfully")
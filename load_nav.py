import requests
import sqlite3

conn = sqlite3.connect("data/nav.db")

cursor = conn.cursor()

cursor.execute("""
    SELECT scheme_code
    FROM fund_master
""")

funds = cursor.fetchall()

conn = sqlite3.connect("data/nav.db")
cursor = conn.cursor()

for (scheme_code,) in funds:

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(url)
    data = response.json()

    scheme_name = data["meta"]["scheme_name"]
    nav = data["data"][0]["nav"]
    nav_date = data["data"][0]["date"]

    cursor.execute("""
        INSERT OR IGNORE INTO nav_history
        (
            scheme_code,
            scheme_name,
            nav,
            nav_date
        )
        VALUES (?, ?, ?, ?)
    """, (
        scheme_code,
        scheme_name,
        nav,
        nav_date
    ))

    if cursor.rowcount == 1:
        print(f"Inserted: {scheme_name}")
    else:
        print(f"Skipped : {scheme_name} (already exists)")

conn.commit()
conn.close()

print("Load completed")
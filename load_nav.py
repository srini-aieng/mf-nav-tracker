import requests
import sqlite3

funds = [
    "120503",
    "118989",
    "122639"
]

conn = sqlite3.connect("data/nav.db")
cursor = conn.cursor()

for scheme_code in funds:

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(url)
    data = response.json()

    scheme_name = data["meta"]["scheme_name"]
    nav = data["data"][0]["nav"]
    nav_date = data["data"][0]["date"]

    cursor.execute("""
        INSERT INTO nav_history
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

    print(f"Inserted: {scheme_name}")

conn.commit()
conn.close()

print("Load completed")
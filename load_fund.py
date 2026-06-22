import sqlite3

print("Program Started")

funds = [
    ("120503", "ICICI Prudential ELSS Tax Saver Fund"),
    ("118989", "SBI ELSS Tax Saver Fund"),
    ("122639", "Nippon India ELSS Tax Saver Fund")
]

conn = sqlite3.connect("data/nav.db")

print("Database Connected")

cursor = conn.cursor()

for scheme_code, scheme_name in funds:

    print(f"Loading {scheme_code}")

    cursor.execute("""
        INSERT OR IGNORE INTO fund_master
        (
            scheme_code,
            scheme_name
        )
        VALUES (?, ?)
    """,
    (
        scheme_code,
        scheme_name
    ))

conn.commit()

print("Commit Completed")

conn.close()

print("Fund master loaded")
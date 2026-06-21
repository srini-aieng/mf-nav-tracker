import sqlite3
from datetime import datetime

conn = sqlite3.connect("data/nav.db")

cursor = conn.cursor()

cursor.execute("""
SELECT
    scheme_code,
    scheme_name,
    nav,
    nav_date
FROM nav_history
ORDER BY scheme_name
""")

rows = cursor.fetchall()

conn.close()

generated_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

html = """
<!DOCTYPE html>
<html>
<p>Last Updated: {generated_time}</p>
<head>
    <title>Mutual Fund NAV Tracker</title>
</head>
<body>
    <h1>Mutual Fund NAV Tracker</h1>

    <table border="1">
        <tr>
            <th>Scheme Code</th>
            <th>Scheme Name</th>
            <th>NAV</th>
            <th>NAV Date</th>
        </tr>
"""

for row in rows:
    html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
        </tr>
    """
html += """
    </table>
</body>
</html>
"""

with open("docs/index.html", "w", encoding="utf-8") as file:
    file.write(html)

print("HTML report generated")
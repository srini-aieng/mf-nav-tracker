import sqlite3
from datetime import datetime

conn = sqlite3.connect("data/nav.db")

cursor = conn.cursor()

cursor.execute("""
SELECT
    Y.scheme_code,
    Y.scheme_name,
    Y.prv_nav,
    Y.cur_nav,
    (Y.cur_nav - Y.prv_nav) AS change,
    CASE
        WHEN Y.prv_nav = 0 THEN NULL
        ELSE ((Y.cur_nav - Y.prv_nav) / Y.prv_nav) * 100
    END AS change_pct,
    Y.nav_date
FROM (
    SELECT DISTINCT
        X.scheme_code,
        X.scheme_name,
        MAX(CASE WHEN X.HELPER = 1 THEN X.nav ELSE 0 END)
            OVER (PARTITION BY X.scheme_code) AS cur_nav,
        MAX(CASE WHEN X.HELPER = 2 THEN X.nav ELSE 0 END)
            OVER (PARTITION BY X.scheme_code) AS prv_nav,
        X.nav_date,
        X.HELPER
    FROM (
        SELECT
            scheme_code,
            scheme_name,
            nav,
            nav_date,
            row_number() OVER (PARTITION BY scheme_code ORDER BY nav_date DESC) AS HELPER
        FROM nav_history
    ) X
    WHERE X.HELPER IN (1, 2)
) Y
WHERE Y.HELPER = 1
ORDER BY Y.scheme_name
""")

rows = cursor.fetchall()

conn.close()

generated_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

total_records = len(rows)

html = f"""
<!DOCTYPE html>
<html>
<p>Total Funds: {total_records}</p>
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
            <th>Previous NAV</th>
            <th>Current NAV</th>
            <th>Change</th>
            <th>Change %</th>
            <th>NAV Date</th>
        </tr>
"""

for row in rows:
    change = row[4]
    change_pct = row[5]
    change_str = f"{change:.4f}" if change is not None else "N/A"
    change_pct_str = f"{change_pct:.2f}%" if change_pct is not None else "N/A"
    html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{change_str}</td>
            <td>{change_pct_str}</td>
            <td>{row[6]}</td>
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
CREATE TABLE IF NOT EXISTS nav_history
(
    scheme_code TEXT,
    scheme_name TEXT,
    nav REAL,
    nav_date TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (scheme_code, nav_date)
);
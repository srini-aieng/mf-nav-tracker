CREATE TABLE IF NOT EXISTS nav_history
(
    scheme_code TEXT,
    scheme_name TEXT,
    nav REAL,
    nav_date TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (scheme_code, nav_date)
);

CREATE TABLE IF NOT EXISTS fund_master
(
    scheme_code TEXT PRIMARY KEY,
    scheme_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS portfolio_transactions
(
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    units REAL NOT NULL,
    amount REAL NOT NULL
);
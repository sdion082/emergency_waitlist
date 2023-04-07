DROP TABLE IF EXISTS waitlist;

CREATE TABLE waitlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    severity INTEGER NOT NULL,
    arrival INTEGER NOT NULL
);
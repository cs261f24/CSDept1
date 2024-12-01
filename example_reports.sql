DROP TABLE IF EXISTS events;
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    event_description TEXT NOT NULL,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME
);

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

DROP TABLE IF EXISTS user_events;
CREATE TABLE IF NOT EXISTS user_events (
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, event_id)
);

DROP TABLE IF EXISTS reports;
CREATE TABLE reports (
    id INTEGER PRIMARY KEY,
    event_type TEXT
    
);
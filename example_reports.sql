/* If a table like reports exists, it is dropped */
DROP TABLE IF EXISTS reports;

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    event TEXT NOT NULL,
    event_type TEXT NOT NULL  -- New column for event type
);

/* If the events table exists, it is dropped */
DROP TABLE IF EXISTS events;

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    event_description TEXT NOT NULL,
    attended INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

/* Example data can be added here to insert into the database */
INSERT INTO reports(name, event, event_type) VALUES('John Smith', 'CS Club Meeting', 'Club');
INSERT INTO reports(name, event, event_type) VALUES('Johnny Smith', 'Xavier Alumni Speaker', 'Guest Speaker');
INSERT INTO reports(name, event, event_type) VALUES('Dan Martin', 'Meeting With Liz', 'Advising Meeting');
INSERT INTO reports(name, event, event_type) VALUES('Jimmy Johnson', 'Outing at St. Vincent DePaul', 'Volunteering');
INSERT INTO reports(name, event, event_type) VALUES('Samuel Williams', 'CS Club Meeting', 'Club');
INSERT INTO reports(name, event, event_type) VALUES('Mary-Kate Williams', 'Basketball Club', 'Sport');

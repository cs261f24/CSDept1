/* If a table like reports exists, it is dropped*/
DROP TABLE IF EXISTS reports;

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    event TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    attended INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

/* Example data can be added here to insert into the database */
INSERT INTO reports(name, event) VALUES('John Smith', 'CS Club');
INSERT INTO reports(name, event) VALUES('Johnny Smith', 'CS Club');
INSERT INTO reports(name, event) VALUES('Dan Martin', 'Volunteering');
INSERT INTO reports(name, event) VALUES('Jimmy Johnson', 'Art Club');
INSERT INTO reports(name, event) VALUES('Samuel Williams', 'Theater Club');

/* If the events table exists, it is dropped */
DROP TABLE IF EXISTS events;


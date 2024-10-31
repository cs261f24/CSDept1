/* If a table like reports exists, it is dropped */
DROP TABLE IF EXISTS reports;
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    event TEXT NOT NULL,
    event_type TEXT NOT NULL,  -- New column for event type
    date_attended DATE NOT NULL

);

DROP TABLE IF EXISTS events;
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    event_description TEXT NOT NULL,
    event_date DATE NOT NULL
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

/* Example data can be added here to insert into the database */
INSERT INTO reports(name, event, event_type, date_attended) VALUES('John Smith', 'CS Club Meeting', 'Club', '2024-09-29');
INSERT INTO reports(name, event, event_type, date_attended) VALUES('Johnny Smith', 'Xavier Alumni Speaker', 'Guest Speaker', '2024-10-20');
INSERT INTO reports(name, event, event_type, date_attended) VALUES('Dan Martin', 'Meeting With Liz', 'Advising Meeting', '2024-10-22');
INSERT INTO reports(name, event, event_type, date_attended) VALUES('Jimmy Johnson', 'Outing at St. Vincent DePaul', 'Volunteering', '2024-10-01');
INSERT INTO reports(name, event, event_type, date_attended) VALUES('Samuel Williams', 'CS Club Meeting', 'Club', '2024-10-21');
INSERT INTO reports(name, event, event_type, date_attended) VALUES('Mary-Kate Williams', 'Basketball Club', 'Sport', '2024-10-27');

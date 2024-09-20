/* If a table like reports exists, it is dropped*/
DROP TABLE IF EXISTS reports;

CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    event TEXT NOT NULL
);

/* Example data can be added here to insert into the database */
INSERT INTO reports(name, event) VALUES('John Smith', 'CS Club');
INSERT INTO reports(name, event) VALUES('Johnny Smith', 'CS Club');
INSERT INTO reports(name, event) VALUES('Dan Martin', 'Volunteering');
INSERT INTO reports(name, event) VALUES('Jimmy Johnson', 'Art Club');
INSERT INTO reports(name, event) VALUES('Samuel Williams', 'Theater Club');
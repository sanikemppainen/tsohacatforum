CREATE TABLE Pictures (
	id SERIAL PRIMARY KEY,
	name TEXT,
	data BYTEA,
	permission INTEGER,
	visible INTEGER
);

CREATE TABLE Users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT,
	admin INTEGER
);

CREATE TABLE Threads (
	id SERIAL PRIMARY KEY,
	topic TEXT,
	userid INTEGER REFERENCES Users ON DELETE CASCADE,
	username TEXT,
	createdat TIMESTAMP,
	tags TEXT,
	preview TEXT 
);

CREATE TABLE Messages (
	id SERIAL PRIMARY KEY,
	message TEXT,
	userid INTEGER REFERENCES Users ON DELETE CASCADE,
	threadid INTEGER REFERENCES Threads ON DELETE CASCADE,
	username TEXT,
	sentat TIMESTAMP
);

CREATE TABLE Votes (
	id SERIAL PRIMARY KEY,
	nameofphoto TEXT,
	votes INTEGER
);


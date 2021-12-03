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

CREATE TABLE Messages (
	id SERIAL PRIMARY KEY,
	message TEXT,
	threadid INTEGER,
	pictureid INTEGER REFERENCES Pictures,
	userid INTEGER REFERENCES Users,
	sentat TIMESTAMP
);

CREATE TABLE Votes (
	id SERIAL PRIMARY KEY,
	votes INTEGER
);

CREATE TABLE Threads (
	id SERIAL PRIMARY KEY,
	topic TEXT,
	userid INTEGER REFERENCES Users,
	createdat TIMESTAMP,
	tags TEXT,
	messageids INTEGER REFERENCES Messages
);

CREATE TABLE ThreadLikes (
	id SERIAL PRIMARY KEY,
	threadid INTEGER REFERENCES Threads,
	votes INTEGER,
	userid INTEGER UNIQUE
);
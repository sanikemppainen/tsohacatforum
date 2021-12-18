CREATE TABLE Pictures (
	id SERIAL PRIMARY KEY,
	name TEXT,
	data BYTEA,
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
	sentat TIMESTAMP,
	pictureid INTEGER REFERENCES Pictures ON DELETE CASCADE,
	picturedata TEXT
);

CREATE TABLE Votes (
	id SERIAL PRIMARY KEY,
	nameofphoto TEXT,
	votes INTEGER
);


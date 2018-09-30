CREATE DATABASE MEI;

USE MEI;

CREATE TABLE Users (
    userID INT AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (userID)
);

CREATE TABLE Project (
    projectID INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    org VARCHAR(255) NOT NULL,
    creationDate DATETIME NOT NULL,
    context VARCHAR(512) NOT NULL,
    owner INT NOT NULL,
    FOREIGN KEY (owner) REFERENCES Users (userID),
    PRIMARY KEY (projectID)
);

CREATE TABLE Session (
    sessionID INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    summary VARCHAR(512) NOT NULL,
    triggeringQuestion VARCHAR(512) NOT NULL,
    creationDate DATETIME NOT NULL,
    project INT NOT NULL,
    FOREIGN KEY (project) REFERENCES Project(projectID),
    PRIMARY KEY (sessionID)
);

CREATE TABLE Role (
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(name)
);

INSERT INTO Role (name) VALUES ('Participant');
INSERT INTO Role (name) VALUES ('Observer');
INSERT INTO Role (name) VALUES ('Documenter');
INSERT INTO Role (name) VALUES ('Facilitator');

CREATE TABLE Member (
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    session INT NOT NULL,
    FOREIGN KEY (session) REFERENCES Session(sessionID),
    FOREIGN KEY (role) REFERENCES Role(name),
    PRIMARY KEY (session, email)
);

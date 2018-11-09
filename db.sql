DROP DATABASE IF EXISTS MEI;

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

CREATE TABLE GeneralStructure (
    structureID INT AUTO_INCREMENT,
    sessionID INT UNIQUE,
    levels JSON,
    PRIMARY KEY (structureID),
    FOREIGN KEY (sessionID) REFERENCES Session(sessionID)
);

CREATE TABLE MatrixValue (
    sessionID INT,
    iRow INT,
    iColumn INT,
    value INT,
    PRIMARY KEY (sessionID, iRow, iColumn),
    FOREIGN KEY (sessionID) REFERENCES Session(sessionID)
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

CREATE TABLE IdeaType (
    name VARCHAR(255) NOT NULL,
    defaultRelationQuestion VARCHAR(255) NOT NULL,
    PRIMARY KEY(name)
);

INSERT INTO IdeaType (name, defaultRelationQuestion) VALUES ('Problem', 'default question for Problem');
INSERT INTO IdeaType (name, defaultRelationQuestion) VALUES ('Objective', 'default question for Objective');
INSERT INTO IdeaType (name, defaultRelationQuestion) VALUES ('Solution', 'default question for Solution');
INSERT INTO IdeaType (name, defaultRelationQuestion) VALUES ('Action', 'default question for Action');
INSERT INTO IdeaType (name, defaultRelationQuestion) VALUES ('Feature', 'default question for Feature');

CREATE TABLE Category (
    categoryID INT AUTO_INCREMENT,
    sessionID INT NOT NULL,
    categoryName VARCHAR(255) NOT NULL,
    PRIMARY KEY (categoryID),
    FOREIGN KEY (sessionID) REFERENCES Session(sessionID)
);

CREATE TABLE CategoryQuestion (
    sessionID INT NOT NULL,
    firstElementID INT NOT NULL,
    secondElementID INT NOT NULL,
    yesVotes INT NOT NULL,
    noVotes INT NOT NULL,
    answer BOOL NOT NULL,
    PRIMARY KEY (sessionID, firstElementID, secondElementID),
    FOREIGN KEY (sessionID) REFERENCES Session(sessionID),
    FOREIGN KEY (firstElementID) REFERENCES Idea(ideaID),
    FOREIGN KEY (secondElementID) REFERENCES Idea(ideaID)
);

CREATE TABLE Idea (
    ideaID INT AUTO_INCREMENT,
    parentIdeaID INT,
    idea VARCHAR(510) NOT NULL,
    clarification  VARCHAR(255),
    participant VARCHAR(255),
    type VARCHAR(255) NOT NULL,
    session INT NOT NULL,
    ideaSessionNumber INT NOT NULL,
    categoryID INT,
    FOREIGN KEY(session, participant) REFERENCES Member(session, email),
    FOREIGN KEY (type) REFERENCES IdeaType(name),
    FOREIGN KEY (session) REFERENCES Session(sessionID),
    FOREIGN KEY (parentIdeaID) REFERENCES Idea (ideaID),
    FOREIGN KEY (categoryID) REFERENCES Category (categoryID),
    PRIMARY KEY (ideaID)
);

CREATE TABLE QuestionAsked (
    sessionID INT NOT NULL,
    firstElement INT NOT NULL,
    secondElement INT NOT NULL,
    yesVotes INT NOT NULL,
    noVotes INT NOT NULL,
    PRIMARY KEY (sessionID, firstElement, secondElement),
    FOREIGN KEY (sessionID) REFERENCES Session (sessionID),
    FOREIGN KEY (firstElement) REFERENCES Idea (ideaID),
    FOREIGN KEY (secondElement) REFERENCES Idea (ideaID)
);

CREATE TABLE RelationshipQuestion (
    sessionID INT NOT NULL,
    ideaType VARCHAR(255) NOT NULL,
    customQuestion VARCHAR(255),
    PRIMARY KEY (sessionID, ideaType),
    FOREIGN KEY (sessionID) REFERENCES Session(sessionID),
    FOREIGN KEY (ideaType) REFERENCES IdeaType(name)
);

CREATE TABLE StructureQuestion (
    structureType VARCHAR(128),
    structureQuestion VARCHAR(255),
    PRIMARY KEY (structureType)
);

INSERT INTO StructureQuestion (structureType, structureQuestion) VALUES ('CAMPO', 'pertenece a la misma cateogría que');
INSERT INTO StructureQuestion (structureType, structureQuestion) VALUES ('PRIORIDAD', 'tiene');

CREATE TABLE Votes (
    voteID INT AUTO_INCREMENT,
    session INT NOT NULL,
    ideaID INT NOT NULL,
    participant VARCHAR(255) NOT NULL,
    ideaPriority INT,
    PRIMARY KEY (voteID)
);

CREATE TABLE VotingDetails (
  session INT NOT NULL,
  votingScheme VARCHAR(255),
  ideasToVote INT,
  PRIMARY KEY (session)
);

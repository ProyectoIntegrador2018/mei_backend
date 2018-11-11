DROP PROCEDURE IF EXISTS CreateElement;
DROP PROCEDURE IF EXISTS GetStructureQuestion;
DROP PROCEDURE IF EXISTS CreateCategory;
DROP PROCEDURE IF EXISTS GetCategoriesIDForSession;
DROP PROCEDURE IF EXISTS GetIdeasInCategory;
DROP PROCEDURE IF EXISTS UpdateCategoryName;
DROP PROCEDURE IF EXISTS UpdateCategoryForIdea;
DROP PROCEDURE IF EXISTS UpdatePriorityForIdea;
DROP PROCEDURE IF EXISTS AddPrioritiesQuestion;

-- Create Element
DELIMITER //
CREATE PROCEDURE CreateElement (IN p_idea VARCHAR(510), IN p_participant VARCHAR(255), IN p_ideaType VARCHAR(32), IN p_sessionID INT)
BEGIN
	DECLARE idea_number INT DEFAULT 1;
	SELECT COUNT(*) + 1 INTO idea_number FROM Idea WHERE session = p_sessionID;
	INSERT INTO Idea (idea, participant, type, session, ideaSessionNumber)
	VALUES (p_idea, p_participant, p_ideaType, p_sessionID, idea_number);
	SELECT LAST_INSERT_ID(), idea_number;
END //

-- Get structure relationship question
DELIMITER //
CREATE PROCEDURE GetStructureQuestion (IN p_structureType VARCHAR(128))
BEGIN
	SELECT structureQuestion FROM StructureQuestion WHERE structureType = p_structureType;
END //

-- Create a category
DELIMITER //
CREATE PROCEDURE CreateCategory (IN p_sessionID INT)
BEGIN
	DECLARE category_number INT DEFAULT 1;
	SELECT COUNT(*) + 1 INTO category_number FROM Category WHERE sessionID = p_sessionID;
	INSERT INTO Category (sessionID, categoryName)
	VALUES (p_sessionID, (SELECT CONCAT("Category ", category_number)));

	SELECT LAST_INSERT_ID();
END //

-- Get categories IDs from a session
DELIMITER //
CREATE PROCEDURE GetCategoriesIDForSession (IN p_sessionID INT)
BEGIN
	SELECT categoryID, categoryName FROM Category WHERE sessionID = p_sessionID;
END //

-- Get ideas in a given category
DELIMITER //
CREATE PROCEDURE GetIdeasInCategory (IN p_sessionID INT, IN p_categoryID INT)
BEGIN
	SELECT ideaID, idea, clarification, type, ideaSessionNumber FROM Idea WHERE session = p_sessionID AND categoryID = p_categoryID;
END //

-- Update category name
DELIMITER //
CREATE PROCEDURE UpdateCategoryName (IN p_categoryID INT, IN p_categoryName VARCHAR(255))
BEGIN
	UPDATE Category
	SET categoryName = p_categoryName
	WHERE categoryID = p_categoryID;
END //

-- Update category for ideas
DELIMITER //
CREATE PROCEDURE UpdateCategoryForIdea (IN p_categoryID INT, IN p_ideaID INT)
BEGIN
	UPDATE Idea
	SET categoryID = p_categoryID
	WHERE ideaID = p_ideaID;
END //

-- Create question answered for priorityes structuring
DELIMITER //
CREATE PROCEDURE AddPrioritiesQuestion (IN p_sessionID INT, IN p_firstElementID INT, IN p_secondElementID INT, IN p_yesVotes INT, IN p_noVotes INT, IN p_sameVotes INT, IN p_answer INT)
BEGIN
	INSERT INTO PriorityQuestion (sessionID, firstElementID, secondElementID, yesVotes, noVotes, sameVotes, answer)
	VALUES (p_sessionID, p_firstElementID, p_secondElementID, p_yesVotes, p_noVotes, p_sameVotes, p_answer);
END //

-- Update priority for ideas
DELIMITER //
CREATE PROCEDURE UpdatePriorityForIdea (IN p_priority INT, IN p_ideaID INT)
BEGIN
	UPDATE Idea
	SET priority = p_priority
	WHERE ideaID = p_ideaID;
END //

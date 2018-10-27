DROP PROCEDURE IF EXISTS CreateElement;

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
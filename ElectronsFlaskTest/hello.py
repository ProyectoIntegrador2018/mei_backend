import bcrypt
import datetime
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
import random
import collections


load_dotenv()

app = Flask(__name__)
cors = CORS(app)
mysql = MySQL()

# CORS configurations
app.config['CORS_HEADERS'] = 'Content-Type'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')

app.secret_key = b'nDnacIzgawo6d4hdRR8y'

mysql.init_app(app)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
	cur = mysql.connect().cursor()
	cur.execute('SELECT * FROM Users')
	r = [dict((cur.description[i][0], value)
		for i, value in enumerate(row)) for row in cur.fetchall()]
	return jsonify({'Users' : r})

@app.route('/get_session_info', methods=['POST'])
def get_session_info():

	connection = mysql.connect()
	cur = connection.cursor()

	session_key = request.form['session_key']
	email = session[session_key]

	select_query = 'SELECT userID, name FROM Users WHERE email = %s'
	data = (email)

	cur.execute(select_query, data)
	row = cur.fetchall()[0] # Only one row should return since email is UNIQUE

	userID, name = row[0], row[1]

	try:
		cur.execute(select_query, data)
		return jsonify({'Success' : True, 'userID' : userID, 'name' : name})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/get_user_projects', methods=['POST'])
def get_user_projects():

	connection = mysql.connect()
	cur = connection.cursor()

	userID = request.form['userID']

	select_query = 'SELECT projectID, name, org, creationDate, context FROM Project  WHERE owner = %s'
	data = (userID)

	cur.execute(select_query, data)
	rows = cur.fetchall()
	r = [dict((cur.description[i][0], value)
			  for i, value in enumerate(row)) for row in rows]

	try:
		cur.execute(select_query, data)
		return jsonify({'Success' : True, 'Projects' : r})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/create_user', methods=['POST'])
def create_user():
	connection = mysql.connect()
	cur = connection.cursor()
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

	select_query = 'SELECT userID FROM Users WHERE email = %s'
	data = (email)

	cur.execute(select_query, data)
	rows = cur.fetchall()

	if len(rows) > 0:
		return jsonify({'Error': 'Email already registered, please use a different one.'})

	insert_query = 'INSERT INTO Users (email, name, password) VALUES (%s, %s, %s)'
	data_to_insert = (email, name, hashed_password)

	try:
		cur.execute(insert_query, data_to_insert)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/login_user', methods=['POST'])
def login_user():
	connection = mysql.connect()
	cur = connection.cursor()
	email = request.form['email']
	password = request.form['password']

	select_query = 'SELECT password FROM Users WHERE email = %s'
	data = (email)

	try:
		cur.execute(select_query, data)
		rows = cur.fetchall()

		# There shouldn't be more than one row with the same email since it's UNIQUE.
		assert len(rows) <= 1

		if len(rows) == 0:
			return jsonify({'Error': 'Email not registered'})

		row = rows[0]
		hashed_password = row[0]

		if bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8')):
			session['email'] = email
			return jsonify({'Success': 'User found!'})
		else:
			return jsonify({'Error': 'Wrong credentials'})

	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/save_project_id', methods=['POST'])
def save_project_id():
	projectID = request.form['projectID']
	session['projectID'] = projectID
	return jsonify({'Success': True})

@app.route('/get_project_info', methods=['POST'])
def get_project_info():
	connection = mysql.connect()
	cur = connection.cursor()
	projectID = request.form['projectID']

	select_query = 'SELECT * FROM Project WHERE projectID = %s'
	data = (projectID)

	try:
		cur.execute(select_query, data)
		row = cur.fetchall()[0]
		creationDate = row[3]
		creationDate = '{}-{:02d}-{:02d}'.format(creationDate.year, creationDate.month, creationDate.day)
		return jsonify({'Success': 'True', 'projectID': row[0], 'projectName': row[1], 'organization': row[2], 'creationDate': creationDate, 'description': row[4]})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/edit_project', methods=['POST'])
def edit_project():
	connection = mysql.connect()
	cur = connection.cursor()
	projectID = request.form['projectID']

	name = request.form['name']
	organization = request.form['org']
	creation_date = request.form['creationDate']
	context = request.form['context']

	update_query = 'UPDATE Project SET name = %s, org =  %s, creationDate = %s, context = %s WHERE projectID = %s'
	data = (name, organization, creation_date, context, projectID)

	try:
		cur.execute(update_query, data)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/create_project', methods=['POST'])
def create_project():
	connection = mysql.connect()
	cur = connection.cursor()

	name = request.form['name']
	organization = request.form['org']
	creation_date = request.form['creationDate']
	context = request.form['context']
	owner = request.form['owner']

	insert_query = 'INSERT INTO Project (name, org, creationDate, context, owner) \
									VALUES (%s, %s, %s, %s, %s)'
	data_to_insert = (name, organization, creation_date, context, owner)

	try:
		cur.execute(insert_query, data_to_insert)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/get_project_sessions', methods=['POST'])
def  get_project_sessions():
	connection = mysql.connect()
	cur = connection.cursor()
	projectID = request.form['projectID']

	select_query = 'SELECT sessionID, name, summary, triggeringQuestion, creationDate FROM Session  WHERE project = %s'
	data = (projectID)
	cur.execute(select_query, data)
	rows = cur.fetchall()
	r = [dict((cur.description[i][0], value)
			  for i, value in enumerate(row)) for row in rows]

	try:
		cur.execute(select_query, data)
		return jsonify({'Success' : True, 'Sessions' : r})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/create_session', methods=['POST'])
def create_session():
	connection = mysql.connect()
	cur = connection.cursor()

	name = request.form['name']
	summary = request.form['summary']
	triggeringQuestion = request.form['triggeringQuestion']
	creationDate = request.form['creationDate']
	projectID = request.form['projectID']

	insert_query = 'INSERT INTO Session (name, summary, triggeringQuestion, creationDate, project) \
									VALUES (%s,%s, %s, %s, %s)'
	data_to_insert = (name, summary, triggeringQuestion, creationDate, projectID)

	try:
		cur.execute(insert_query, data_to_insert)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/delete_participant', methods=['POST'])
def delete_participant():
	connection = mysql.connect()
	cur = connection.cursor()

	email = request.form['email']
	sessionID = request.form['sessionID']

	query = 'DELETE FROM Member WHERE email = %s AND session = %s'
	data = (email, sessionID)

	try:
		cur.execute(query, data)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/edit_participant', methods=['POST'])
def edit_participant():
	connection = mysql.connect()
	cur = connection.cursor()

	name = request.form['name']
	previous_email = request.form['previous_email']
	new_email = request.form['new_email']
	role = request.form['role']
	sessionID = request.form['sessionID']

	query = 'UPDATE Member SET name = %s, email = %s, role = %s WHERE email = %s AND session = %s'
	data = (name, new_email, role, previous_email, sessionID)

	try:
		cur.execute(query, data)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/create_participant', methods=['POST'])
def create_participant():
	connection = mysql.connect()
	cur = connection.cursor()

	name = request.form['name']
	email = request.form['email']
	role = request.form['role']
	sessionID = request.form['sessionID']

	query = 'INSERT INTO Member (name, email, role, session) VALUES (%s, %s, %s, %s)'
	data = (name, email, role, sessionID)

	try:
		cur.execute(query, data)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		print(e)
		return jsonify({'Error': str(e)})

@app.route('/get_session_participants', methods=['POST'])
def get_session_participants():
	connection = mysql.connect()
	cur = connection.cursor()

	sessionID = request.form['sessionID']

	query = 'SELECT * FROM Member WHERE session = %s'
	data = (sessionID)

	try:
		cur.execute(query, data)
		rows = cur.fetchall()
		r = [dict((cur.description[i][0], value)
				  for i, value in enumerate(row)) for row in rows]
		return jsonify({'Success': True, 'Members': r})
	except Exception as e:
		print(e)
		return jsonify({'Error': str(e)})

@app.route('/get_participant_information', methods=['POST'])
def get_participant_information():
	connection = mysql.connect()
	cur = connection.cursor()

	sessionID = request.form['sessionID']
	email = request.form['email']

	query = 'SELECT * FROM Member WHERE email = %s AND session = %s'
	data = (email, sessionID)

	try:
		cur.execute(query, data)
		row = cur.fetchall()[0] # Only one user should be returned since the primary key is (sessionID, email)
		return jsonify({'Success': True, 'name': row[0], 'role': row[2], 'email': row[1]})
	except Exception as e:
		print(e)
		return jsonify({'Error': str(e)})

@app.route('/copy_session_participants', methods=['POST'])
def copy_session_participants():
	connection = mysql.connect()
	cur = connection.cursor()

	sessionID = request.form['sessionID']
	copy_from_sessionID = request.form['copyFromSessionID']

	query = 'SELECT name, email, role FROM ((SELECT name, email, role FROM Member WHERE session = %s) UNION (SELECT name, email, role FROM Member WHERE session = %s)) AS memberunion WHERE email NOT IN (SELECT email FROM Member WHERE session = %s)'
	data = (copy_from_sessionID, sessionID, sessionID)

	insert_query = 'INSERT INTO Member (name, email, role, session) VALUES (%s, %s, %s, %s)'

	try:
		cur.execute(query, data)
		participants_to_insert = cur.fetchall() # Participants that are in session to copy from and are not already registered in the session to copy to
		print(participants_to_insert)
		for participant in participants_to_insert:
			name, email, role = participant[0], participant[1], participant[2]
			data_to_insert = (name, email, role, sessionID)
			print(data_to_insert)
			cur.execute(insert_query, data_to_insert)

		connection.commit()

		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/get_session_data', methods=['POST'])
def get_session_data():
	connection = mysql.connect()
	cur = connection.cursor()
	sessionID = request.form['sessionID']
	select_query = 'SELECT * FROM Session WHERE sessionID = %s'
	data = (sessionID)

	try:
		cur.execute(select_query, data)
		row = cur.fetchall()[0]
		creationDate = row[4]
		creationDate = '{}-{:02d}-{:02d}'.format(creationDate.year, creationDate.month, creationDate.day)
		return jsonify({'Success': 'True', 'sessionID': row[0], 'name': row[1], 'summary': row[2], 'triggeringQuestion'	: row[3], 'creationDate': creationDate})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/get_participant_types', methods=['POST'])
def get_participant_types():
	connection = mysql.connect()
	cur = connection.cursor()
	select_query = 'SELECT * FROM Role'

	try:
		cur.execute(select_query)
		rows = cur.fetchall()
		r = [dict((cur.description[i][0], value)
			  for i, value in enumerate(row)) for row in rows]
		return jsonify({'Success': True, 'Roles': r})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/edit_session', methods=['POST'])
def edit_session():
	connection = mysql.connect()
	cur = connection.cursor()
	sessionID = request.form['sessionID']
	name = request.form['name']
	summary = request.form['summary']
	triggeringQuestion = request.form['triggeringQuestion']
	creationDate = request.form['creationDate']

	update_query = 'UPDATE Session SET name = %s, summary =  %s, triggeringQuestion = %s, creationDate = %s WHERE sessionID = %s'
	data = (name, summary, triggeringQuestion, creationDate, sessionID)

	try:
		cur.execute(update_query, data)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/get_session_ideas', methods=['POST'])
def get_session_ideas():
	connection = mysql.connect()
	cur = connection.cursor()
	sessionID = request.form['sessionID']

	query_parents = 'SELECT * FROM Idea WHERE session = %s AND parentIdeaID IS NULL'
	query_children = 'SELECT * FROM Idea WHERE session = %s AND parentIdeaID IS NOT NULL'
	data = (sessionID)
	try:
		cur.execute(query_parents, data)
		parent_rows = cur.fetchall()

		cur.execute(query_children, data)
		child_rows = cur.fetchall()

		ideas = dict()

		for parent in parent_rows:
			parentID = parent[0]
			ideas[parentID] = [parent] + list(filter(lambda x: x is not None , list(map(lambda child: child if child[1] == parentID else None, child_rows))))

		return jsonify({'Success': True, 'Ideas': ideas})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/get_all_session_ideas', methods=['POST'])
def get_all_session_ideas():
	connection = mysql.connect()
	cur = connection.cursor()
	sessionID = request.form['sessionID']

	query_ideas = 'SELECT * FROM Idea WHERE session = %s ORDER BY ideaSessionNumber'
	data = (sessionID)
	try:
		cur.execute(query_ideas, data)
		rows = cur.fetchall()

		ideas = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in rows]

		return jsonify({'Success': True, 'Ideas': ideas})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/join_ideas', methods=['POST'])
def join_ideas():
	connection = mysql.connect()
	cur = connection.cursor()
	query = 'Update IDEA SET parentIdeaID = %s WHERE ideaID = %s'
	try:
		# Reset all parent/child relationship
		for key, value in request.form.items():
			if (key  != 'sessionID'):
				ideaID = int(key[key.find('[') + 1 : key.find(']')])
				data = (None, ideaID)
				cur.execute(query, data)

		# Set parentIdeaID for all child ideas
		for key, value in request.form.items():
			if (key  != 'sessionID'):
				parentIdeaID = int(key[key.find('[') + 1 : key.find(']')])
				childIdeas = list(map(lambda childIdeaID: int(childIdeaID), request.form.getlist(key)[1:]))
				for childIdeaID in childIdeas:
					data = (parentIdeaID, childIdeaID)
					cur.execute(query, data)

		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error', str(e)})

@app.route('/update_clarification', methods=['POST'])
def update_clarification():
	connection = mysql.connect()
	cur = connection.cursor()
	ideaID = request.form['ideaID']
	clarification = request.form['clarification']

	query = 'UPDATE Idea SET clarification = %s WHERE ideaID = %s'
	data = (clarification, ideaID)

	try:
		cur.execute(query, data)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/create_element', methods=['POST'])
def create_element():
	connection = mysql.connect()
	cur = connection.cursor()
	print(request.form)
	idea = request.form['idea']
	participant = request.form['participant'] if request.form['participant'] != '' else None
	ideaType = request.form['ideaType']
	sessionID = request.form['sessionID']

	try:
		cur.callproc('CreateElement', (idea, participant, ideaType, sessionID))
		row = cur.fetchall()
		connection.commit()
		return jsonify({'Success': True, 'ideaID': row[0][0], 'ideaNumber': row[0][1]})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/set_voting_details', methods=['POST'])
def set_voting_details():
	connection = mysql.connect()
	cur = connection.cursor()
	sessionID = request.form['sessionID']
	votingScheme = request.form['votingScheme']
	ideasToVote = request.form['ideasToVote']

	print(sessionID,votingScheme,ideasToVote)

	query = 'INSERT INTO VotingDetails (sessionID, votingScheme, ideasToVote) VALUES (%s, %s, %s)'
	data = (sessionID, votingScheme, ideasToVote)

	try:
		cur.execute(query, data)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		print(e)
		return jsonify({'Error': str(e)})

@app.route('/get_voting_details', methods=['POST'])
def get_voting_details():
	connection = mysql.connect()
	cur = connection.cursor()
	sessionID = request.form['sessionID']

	query_details = 'SELECT * FROM VotingDetails WHERE sessionID = %s'
	data = (sessionID)

	try:
		cur.execute(query_details, data)
		rows = cur.fetchall()

		details = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in rows]
		print(details)
		if len(details) > 0:
			return jsonify({'Success': True, 'votingDetails': details})
		else:
			return jsonify({'Success': False, 'votingDetails': details})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/get_parent_ideas', methods=['POST'])
def get_parent_ideas():
	connection = mysql.connect()
	cur = connection.cursor()
	sessionID = request.form['sessionID']

	query_parents = 'SELECT ideaID,idea FROM Idea WHERE session = %s AND parentIdeaID IS NULL ORDER BY ideaID'
	data = (sessionID)
	try:
		cur.execute(query_parents, data)
		parent_rows = cur.fetchall()
		print(parent_rows)
		ideasIds = []
		ideasTexts = []

		for parent in parent_rows:
			parentID = parent[0]
			print(parentID)
			parentText = parent[1]
			print(parentText)
			ideasIds.append(parentID)
			ideasTexts.append(parentText)

		print(ideasIds,ideasTexts)

		return jsonify({'Success': True, 'ideasIDs': ideasIds, 'ideasText':ideasTexts})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/get_first_ideaID', methods=['POST'])
def get_first_ideaID():
	connection = mysql.connect()
	cur = connection.cursor()
	sessionID = request.form['sessionID']

	query_parents = 'SELECT ideaID FROM Idea WHERE session = %s ORDER BY ideaID LIMIT 1'
	data = (sessionID)
	try:
		cur.execute(query_parents, data)
		row = cur.fetchall()

		print(row[0][0])

		return jsonify({'Success': True, 'firstID': row[0][0]})
	except Exception as e:
		return jsonify({'Error': str(e)})

@app.route('/save_vote', methods=['POST'])
def save_vote():
	connection = mysql.connect()
	cur = connection.cursor()

	print(request.form)

	session = request.form['sessionID']
	ideaPriority = request.form['vote']
	ideaID = request.form['ideaID']
	participant = request.form['member']

	data = (session, ideaID, participant, ideaPriority)
	insert_query = 'INSERT INTO Votes (session, ideaID, participant, ideaPriority) VALUES (%s, %s, %s, %s)'

	try:
		cur.execute(insert_query, data)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		print(e)
		return jsonify({'Error': str(e)})

@app.route('/get_voting_results', methods=['POST'])
def get_voting_results():
	connection = mysql.connect()
	cur = connection.cursor()

	print(request.form)

	session = request.form['sessionID']
	votingScheme = request.form['votingScheme']
	ideasToVote = request.form['ideasToVote']

	data = (session)
	select_query = 'SELECT ideaID,ideaPriority FROM Votes WHERE session = %s'

	try:
		cur.execute(select_query, data)
		votes = cur.fetchall()
		procesed_votes = processVotes(votes,votingScheme,ideasToVote)
		return jsonify({'Success': True, 'votes':procesed_votes})
	except Exception as e:
		print(e)
		return jsonify({'Error': str(e)})


def processVotes(votes,votingScheme,ideasToVote):
	voting_results = dict()
	sorted_ideas = []

	print("Votes",votes)

	for vote in votes:
		ideaID = vote[0]
		ideaPriority = vote[1]

		if ideaID in voting_results:
			voting_results[ideaID][0] += 1
			voting_results[ideaID][1] += ideaPriority
		else:
			voting_results[ideaID] = [1,ideaPriority,ideaID]

	unsorted_votes = voting_results.values()
	firstSortValues = sorted(unsorted_votes, key=lambda x: x[0], reverse = True)

	print("FirstSorted",firstSortValues)

	voting_results = collections.OrderedDict()

	for vote in firstSortValues:
		if vote[0] in voting_results:
			voting_results[vote[0]].append(vote)
		else:
			voting_results[vote[0]] = [vote]

	if votingScheme == "x_ideas":
		for vote in firstSortValues:
			for idea in vote:
				sorted_ideas.append[idea[2]]
		print(sorted_ideas)
		return sorted_ideas

	for votes in voting_results:
		voting_results[votes] = sorted(voting_results[votes],key=lambda x: x[1])

	for votes in voting_results:
		for ideas in voting_results[votes]:
			sorted_ideas.append(ideas[2])

	print("VotingResults",sorted_ideas)

	return sorted_ideas

if __name__ == '__main__':
	app.run(debug=True)

import bcrypt
import datetime
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL

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
		return jsonify({'Error': True})

@app.route('/get_user_projects', methods=['POST'])
def get_user_projects():

	connection = mysql.connect()
	cur = connection.cursor()

	userID = request.form['userID']
	
	select_query = 'SELECT name, org, creationDate, context FROM Project  WHERE owner = %s'
	data = (userID)
	
	cur.execute(select_query, data)
	rows = cur.fetchall()
	r = [dict((cur.description[i][0], value)
			  for i, value in enumerate(row)) for row in rows]
	
	try:
		cur.execute(select_query, data)
		return jsonify({'Success' : True, 'Projects' : r})
	except Exception as e:
		return jsonify({'Error': True})

@app.route('/create_user', methods=['POST'])
def create_user():
	connection = mysql.connect()
	cur = connection.cursor()
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

	insert_query = 'INSERT INTO Users (email, name, password) VALUES (%s, %s, %s)'
	data_to_insert = (email, name, hashed_password)

	try:
		cur.execute(insert_query, data_to_insert)
		connection.commit()
		return jsonify({'Success': True})
	except Exception as e:
		return jsonify({'Error': True})

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
		print(e)
		return 'Error'

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
		return jsonify({'Error': True})

if __name__ == '__main__':
	app.run(debug=True)
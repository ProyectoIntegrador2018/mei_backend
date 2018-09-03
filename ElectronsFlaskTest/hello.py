import firebase_admin
import os
from dotenv import load_dotenv
from firebase_admin import credentials
from firebase_admin import db
from flask import Flask

load_dotenv()

firebase_admin.initialize_app(
		credentials.Certificate({
			'type': os.getenv('TYPE'),
			'project_id': os.getenv('PROJECT_ID'),
			'token_uri': os.getenv('TOKEN_URI'),
			'client_email': os.getenv('CLIENT_EMAIL'),
			'private_key': os.getenv('PRIVATE_KEY').replace('\\n', '\n')
		})
	,{
		'databaseURL': os.getenv('DATABASE_URL')
	}
)

app = Flask(__name__)

@app.route('/')
def hello_world():
	ref = db.reference('nombres')
	snapshot = ref.get()
	data = ''
	for key, val in snapshot.items():
		data += ('<li>{0} - {1}</li>\n'.format(key, val))

	return data
import bcrypt
import datetime
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL

class Session:
    id = -1
    summary = ""
    creation_date = ""
    projectId = -1

    def __init__(self, id, summary, creation_date, projectId):
        self.id = id
        self.summary = summary
        self.creation_date = creation_date
        self.projectId = projectId

def CreateSession(session, cursor, connection):
    insert_query = 'INSERT INTO Session (summary, creation_date, projectId) \
                                VALUES (%s, %s, %s, %s, %s)'
    data_to_insert = (session.summary, session.creation_date, session.projectId)

    try:
        cursor.execute(insert_query,data_to_insert)
        connection.commit()
        return jsonify({'Success': True})
    except Exception as e:
        return jsonify({'Error': True})

import bcrypt
import datetime
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL

class Project:
    id = -1
    name = ""
    organization = ""
    creation_date = ""
    context = ""
    owner = ""

    def __init__(self, id, name, organization, creation_date, context, owner):
        self.id = id
        self.name = name
        self.organization = organization
        self.creation_date = creation_date
        self.context = context
        self.owner = owner

def CreateProject(project, cursor, connection):
    insert_query = 'INSERT INTO Project (name, org, creationDate, context, owner) \
                                VALUES (%s, %s, %s, %s, %s)'
    data_to_insert = (project.name, project.organization, project.creation_date, project.context, project.owner)

    try:
        cursor.execute(insert_query,data_to_insert)
        connection.commit()
        return jsonify({'Success': True})
    except Exception as e:
        return jsonify({'Error': True})

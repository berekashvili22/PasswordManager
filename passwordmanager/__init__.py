from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a0e27327a62069c1f3f059bbb7605b09'
app.config['SQLACHEMY_DATABE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 

from passwordmanager import routes
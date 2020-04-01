from flask import Flask 
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'very-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
db = SQLAlchemy(app)
login = LoginManager(app)

import routes 

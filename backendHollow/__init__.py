from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
CORS(app, supports_credentials=True)
app.secret_key = 'de0b6d1205e578d7d79857e211e48182f8167878f4f6ad4b8cf6a7b447cab84c'
app.config['MONGO_URI'] = "mongodb+srv://juokx1:ivhcJlPAiN1QnVsj@wikisherman.ewhecfi.mongodb.net/hollowDB?retryWrites=true&w=majority"
app.config['WTF_CSRF_ENABLED'] = False
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

from backendHollow import routes

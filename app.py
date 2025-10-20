from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
import os
from database import db
from urllib.parse import quote_plus

load_dotenv()

app = Flask(__name__)
CORS(app)

username = os.getenv("DB_USERNAME")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:6543/postgres?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

api = Api(app)

from models import *
from routes import *

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=9909, debug=True, host='0.0.0.0')
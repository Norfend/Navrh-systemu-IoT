import os

from flask import Flask
from dotenv import load_dotenv

from model.temperature_data import Temperature as Data
from model.users_data import User
from utils.configuration import setup_routes
from utils.database import db

load_dotenv()
data_base = Data()
user_base = User()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///temperature_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('TRACK_MODIFICATIONS')

db.init_app(app)
setup_routes(app, db)

if __name__ == "__main__":
    app.run()
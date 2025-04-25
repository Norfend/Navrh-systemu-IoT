import os

from flask import Flask
from dotenv import load_dotenv

from model.temperature_data import Temperature as Data
from model.users_data import User
from controller.routes import setup_routes

load_dotenv()
data_base = Data()
user_base = User()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

setup_routes(app, data_base, user_base)

if __name__ == "__main__":
    app.run()
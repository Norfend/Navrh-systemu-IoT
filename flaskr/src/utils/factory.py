from flask import Flask, redirect, request, url_for, jsonify
from flask_login import LoginManager
from dotenv import load_dotenv
import os

from model.User import User
from utils.configuration import setup_routes
from utils.database import db

login_manager = LoginManager()

def create_app():
    load_dotenv()
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    template_dir = os.path.join(root_path, 'templates')
    static_dir = os.path.join(root_path, 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('TRACK_MODIFICATIONS')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login_controller"
    login_manager.login_message_category = "danger"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.accept_mimetypes.accept_html and not request.path.startswith('/api'):
            return redirect(url_for('login_controller'))
        return jsonify({'error': 'Unauthorized access'}), 401

    setup_routes(app, db)
    return app
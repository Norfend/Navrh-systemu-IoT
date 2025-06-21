import logging
import os
import time
from logging.config import dictConfig

from flask import Flask, redirect, request, url_for, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from dotenv import load_dotenv

from model.User import User
from utils.configuration import setup_routes, setup_mqtt_listener
from utils.database import db
from utils.hardware_state import application_state

login_manager = LoginManager()
logger = logging.getLogger('requests')

def create_app():
    load_dotenv()
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    template_dir = os.path.join(root_path, 'templates')
    static_dir = os.path.join(root_path, 'static')

    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(name)s: %(message)s', }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'default',
                'level': 'INFO'},
            'file' : {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(root_path, 'logs/log.app'),
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 1,
                'formatter': 'default',
                'level': 'DEBUG'}
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    })

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = os.getenv("SECRET_KEY", 'my_super_secret_key_123456')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('TRACK_MODIFICATIONS', 'false')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login_controller"
    login_manager.login_message_category = "danger"

    application_state['start_time'] = time.time()
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri="memory://",
        default_limits=["200 per day", "50 per hour"]
    )

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.accept_mimetypes.accept_html and not request.path.startswith('/api'):
            return redirect(url_for('login_controller'))
        return jsonify({'error': 'Unauthorized access'}), 401

    @app.before_request
    def log_request_info():
        application_state['request_count'] += 1
        logger.debug(f"Incoming request: {request.method} {request.url}")

    setup_routes(app, limiter, db)
    setup_mqtt_listener()
    return app
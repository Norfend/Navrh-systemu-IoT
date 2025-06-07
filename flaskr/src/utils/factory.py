import os
import paho.mqtt.client as mqtt
import requests

from flask import Flask, redirect, request, url_for, jsonify
from flask_login import LoginManager
from dotenv import load_dotenv

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
    app.secret_key = os.getenv("SECRET_KEY", 'my_super_secret_key_123456')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('TRACK_MODIFICATIONS', 'false')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login_controller"
    login_manager.login_message_category = "danger"

    mqtt_broker = 'localhost'
    mqtt_port = 1883
    mqtt_topic = 'sensor/temperature'

    # MQTT client callbacks
    def on_connect(client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe(mqtt_topic, qos=1)

    def on_message(client, userdata, msg):
        print(f"Received message on topic {msg.topic}")
        try:
            data = msg.payload.decode()
            parts = {}
            for part in data.split(", "):
                key, value = part.split(": ", 1)
                parts[key] = value

            payload = {
                "temperature": float(parts["Temperature"]),
                "measurement_time": parts["Measurement Time"],
                "sending_time": parts["Sending Time"]
            }

            response = requests.post("http://localhost:5000/api/add_temperature", json=payload)
        except Exception as e:
            print(f"Error: {e}")

    # Set up MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)

    mqtt_client.loop_start()  # Start the loop to listen for messages

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
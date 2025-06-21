import paho.mqtt.client as mqtt
import requests

from controller.api_routes import temperature_routes
from controller.hardware_routes import hardware_routes
from controller.routes import all_routes
from controller.user_routes import user_routes

mqtt_broker = 'localhost'
mqtt_port = 1883

def setup_routes(app, limiter, db):
    with app.app_context():
        db.create_all()

    all_routes(app, limiter)
    temperature_routes(app)
    user_routes(app)
    hardware_routes(app)

def setup_mqtt_listener():
    mqtt_topic = 'sensor/temperature'

    def on_connect(client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe(mqtt_topic, qos=1)

    def on_message(client, userdata, msg):
        try:
            data = msg.payload.decode()
            parts = data.split(",")

            payload = {
                "measurement_time": parts[0],
                "sending_time": parts[1],
                "temperature": float(parts[2])
            }

            response = requests.post("http://localhost:5000/api/add_temperature", json=payload)
        except Exception as e:
            print(f"Error: {e}")

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)

    mqtt_client.loop_start()

def check_mqtt(broker='localhost', port=1883, timeout=3):
    client = mqtt.Client()
    try:
        client.connect(broker, port, keepalive=timeout)
        client.disconnect()
        return True
    except Exception:
        return False
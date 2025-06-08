from flask import jsonify
from paho.mqtt import publish

from utils.hardware_state import hardware_state as state

mqtt_broker = 'localhost'
mqtt_port = 1883
topics = {
    "led": "control/led",
    "measurement": "control/measurement",
    "interval": "control/interval"
}

def turn_on_measurements_service():
    try:
        publish.single(topics.get("measurement"), payload='on', hostname=mqtt_broker)
        state["measurement"] = True
        return "OK", 200
    except Exception as e:
        return str(e), 500

def turn_off_measurements_service():
    try:
        publish.single(topics.get("measurement"), payload='off', hostname=mqtt_broker)
        state["measurement"] = False
        return "OK", 200
    except Exception as e:
        return str(e), 500

def turn_on_led_service():
    try:
        publish.single(topics.get("led"), payload='on', hostname=mqtt_broker)
        state["led"] = True
        return "OK", 200
    except Exception as e:
        return str(e), 500

def turn_off_led_service():
    try:
        publish.single(topics.get("led"), payload='off', hostname=mqtt_broker)
        state["led"] = False
        return "OK", 200
    except Exception as e:
        return str(e), 500

def set_measurements_interval_service(interval : int):
    try:
        if not (1 <= interval <= 3600):
            return jsonify({"error": "Interval must be an integer between 1 and 3600"}), 400

        publish.single(topics.get("interval"), payload=str(interval), hostname=mqtt_broker)
        state["interval"] = interval
        return jsonify({"message": "Interval updated successfully"}), 200

    except Exception as e:
        return str(e), 500

def get_hardware_status_service():
    return jsonify(state)
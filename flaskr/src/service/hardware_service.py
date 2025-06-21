import logging
import time

from flask import jsonify
from paho.mqtt import publish

from utils.database import check_database
from utils.hardware_state import hardware_state as state, application_state

module_logger = logging.getLogger(__name__)

mqtt_broker = 'localhost'
mqtt_port = 1883
topics = {
    "led": "control/led",
    "measurement": "control/measurement",
    "interval": "control/interval"
}

def turn_on_measurements_service():
    module_logger.debug("Request to turn ON measurements service received")
    try:
        publish.single(topics.get("measurement"), payload='on', hostname=mqtt_broker)
        state["measurement"] = True
        module_logger.info("Measurements service turned ON successfully")
        return "OK", 200
    except Exception as e:
        module_logger.error(f"Failed to turn ON measurements service: {e}", exc_info=True)
        return str(e), 500

def turn_off_measurements_service():
    module_logger.debug("Request to turn OFF measurements service received")
    try:
        publish.single(topics.get("measurement"), payload='off', hostname=mqtt_broker)
        state["measurement"] = False
        module_logger.info("Measurements service turned OFF successfully")
        return "OK", 200
    except Exception as e:
        module_logger.error(f"Failed to turn OFF measurements service: {e}", exc_info=True)
        return str(e), 500

def turn_on_led_service():
    module_logger.debug("Request to turn ON LED service received")
    try:
        publish.single(topics.get("led"), payload='on', hostname=mqtt_broker)
        state["led"] = True
        module_logger.info("LED turned ON successfully")
        return "OK", 200
    except Exception as e:
        module_logger.error(f"Failed to turn ON LED: {e}", exc_info=True)
        return str(e), 500

def turn_off_led_service():
    module_logger.debug("Request to turn OFF LED service received")
    try:
        publish.single(topics.get("led"), payload='off', hostname=mqtt_broker)
        state["led"] = False
        module_logger.info("LED turned OFF successfully")
        return "OK", 200
    except Exception as e:
        module_logger.error(f"Failed to turn OFF LED: {e}", exc_info=True)
        return str(e), 500

def set_measurements_interval_service(interval : int):
    module_logger.debug(f"Request to set measurements interval to {interval}")
    try:
        if not (1 <= interval <= 3600):
            module_logger.warning(f"Invalid interval received: {interval}")
            return jsonify({"error": "Interval must be an integer between 1 and 3600"}), 400

        publish.single(topics.get("interval"), payload=str(interval), hostname=mqtt_broker)
        state["interval"] = interval
        module_logger.info(f"Measurement interval set to {interval} seconds")
        return jsonify({"message": "Interval updated successfully"}), 200

    except Exception as e:
        module_logger.error(f"Failed to set measurements interval: {e}", exc_info=True)
        return str(e), 500

def get_hardware_status_service():
    module_logger.debug("Request to get current hardware status received")
    return jsonify(state)

def get_health_service():
    from utils.configuration import check_mqtt
    db_status = check_database()
    mqtt_status = check_mqtt()
    uptime_seconds = int(time.time() - application_state['start_time'])

    status_code = 200 if db_status and mqtt_status else 503
    response = {
        "database": "online" if db_status else "unreachable",
        "mqtt_broker": "online" if mqtt_status else "unreachable",
        "uptime_seconds": uptime_seconds,
        "processed_requests": application_state['request_count']
    }

    return jsonify(response), status_code
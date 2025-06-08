from flask import request, jsonify

from service.hardware_service import (turn_on_measurements_service, turn_off_measurements_service, turn_on_led_service,
                                      turn_off_led_service, set_measurements_interval_service,
                                      get_hardware_status_service)


def hardware_routes(app):
    @app.route("/api/turn_on_measurements", methods=["POST"])
    def turn_on_measurements_controller():
        return turn_on_measurements_service()

    @app.route("/api/turn_off_measurements", methods=["POST"])
    def turn_off_measurements_controller():
        return turn_off_measurements_service()

    @app.route("/api/turn_on_led", methods=["POST"])
    def turn_on_led_controller():
        return turn_on_led_service()

    @app.route("/api/turn_off_led", methods=["POST"])
    def turn_off_led_controller():
        return turn_off_led_service()

    @app.route("/api/set_measurements_interval", methods=["POST"])
    def set_measurements_interval_controller():
        data = request.get_json()
        if not data or 'interval' not in data:
            return jsonify({"error": "Interval value is required"}), 400
        interval = data.get('interval')
        return set_measurements_interval_service(interval)

    @app.route("/api/status", methods=["GET"])
    def get_hardware_status_controller():
        return get_hardware_status_service()
from flask import request, jsonify

from repository.temperatureRepository import add_temperature, get_last_temperature

def temperature_routes(app):

    @app.route("/api/add_temperature", methods=["POST"])
    def add_temperature_controller():
        data = request.get_json()
        if not data or 'temperature' not in data:
            return jsonify({"error": "Temperature value is required"}), 400

        temperature_value = data.get('temperature')
        return add_temperature(temperature_value)

    @app.route("/api/get_last_temperature", methods=["GET"])
    def get_last_temperature_controller():
        return get_last_temperature()
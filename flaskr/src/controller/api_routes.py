from flask_login import login_required
from flask import request, jsonify

from repository.temperature_repository import add_temperature, get_last_temperature, get_temperature_by_id, \
    delete_last_temperature, delete_temperature_by_id, get_all_temperatures_by_sorting


def temperature_routes(app):
    @app.route("/api/add_temperature", methods=["POST"])
    def add_temperature_controller():
        data = request.get_json()
        if not data or 'temperature' not in data:
            return jsonify({"error": "Temperature value is required"}), 400

        temperature_value = data.get('temperature')
        measurement_time = data.get('measurement_time')
        sending_time = data.get('sending_time')
        return add_temperature(temperature_value, measurement_time, sending_time)

    @app.route("/api/get_last_temperature", methods=["GET"])
    def get_last_temperature_controller():
        return get_last_temperature()

    @app.route("/api/get_temperature_by_id/<int:temperature_id>", methods=["GET"])
    def get_temperature_by_id_controller(temperature_id):
        return get_temperature_by_id(temperature_id)

    @app.route("/api/delete_last_temperature", methods=["POST"])
    @login_required
    def delete_last_temperature_controller():
        return delete_last_temperature()

    @app.route("/api/delete_temperature_by_id/<int:temperature_id>", methods=["POST"])
    @login_required
    def delete_temperature_by_id_controller(temperature_id):
        return delete_temperature_by_id(temperature_id)

    @app.route('/api/get_all_temperatures_by_sorting/<string:sort_order>', methods=['GET'])
    def get_all_temperatures_by_sorting_controller(sort_order):
        return get_all_temperatures_by_sorting(sort_order)
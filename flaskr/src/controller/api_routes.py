import logging

from flask_login import login_required
from flask import request, jsonify

from service.temperature_service import (add_temperature_service, get_last_temperature_service,
                                         get_temperature_by_id_service, delete_last_temperature_service,
                                         delete_temperature_by_id_service, get_all_temperatures_by_sorting_service)

module_logger = logging.getLogger(__name__)

def temperature_routes(app):
    @app.route("/api/add_temperature", methods=["POST"])
    def add_temperature_controller():
        return add_temperature_service(request.get_json())

    @app.route("/api/get_last_temperature", methods=["GET"])
    def get_last_temperature_controller():
        return get_last_temperature_service()

    @app.route("/api/get_temperature_by_id/<int:temperature_id>", methods=["GET"])
    def get_temperature_by_id_controller(temperature_id):
        return get_temperature_by_id_service(temperature_id)

    @app.route("/api/delete_last_temperature", methods=["POST"])
    @login_required
    def delete_last_temperature_controller():
        return delete_last_temperature_service()

    @app.route("/api/delete_temperature_by_id/<int:temperature_id>", methods=["POST"])
    @login_required
    def delete_temperature_by_id_controller(temperature_id):
        return delete_temperature_by_id_service(temperature_id)

    @app.route('/api/get_all_temperatures_by_sorting/<string:sort_order>', methods=['GET'])
    def get_all_temperatures_by_sorting_controller(sort_order):
        return get_all_temperatures_by_sorting_service(sort_order)
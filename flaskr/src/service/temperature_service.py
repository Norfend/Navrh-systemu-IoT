import logging

from flask import jsonify

from repository.temperature_repository import (add_temperature, get_last_temperature, get_temperature_by_id,
                                               delete_last_temperature, delete_temperature_by_id,
                                               get_all_temperatures_by_sorting, get_last_temperatures)

module_logger = logging.getLogger(__name__)

def add_temperature_service(data):
    module_logger.debug("Received request to add a new temperature")
    if not data or ('temperature_value' or 'measurement_time' or 'sending_time') not in data:
        module_logger.warning("Request body is empty or temperature field is missing in request")
        return jsonify({"error": "Temperature value is required"}), 400

    temperature_value = data.get('temperature')
    measurement_time = data.get('measurement_time')
    sending_time = data.get('sending_time')

    try:
        response, status_code = add_temperature(temperature_value, measurement_time, sending_time)
        if status_code == 201:
            module_logger.info(f"Adding temperature value: {temperature_value}, "f"measurement_time: {measurement_time}, sending_time: {sending_time}")
        else:
            module_logger.error(f"Failed to add temperature: {response.get_json().get("error")}")
        return response, status_code
    except Exception as e:
        module_logger.error(f"Exception occurred while adding temperature: {e}", exc_info=True)
        return jsonify({"error": "Temperature wasn't added"}), 500

def get_last_temperature_service():
    module_logger.debug("Request received to fetch the last temperature record")
    try:
        response, status_code = get_last_temperature()
        if status_code == 200:
            module_logger.info("Successfully fetched the last recorded temperature")
        else:
            module_logger.error(f"Failed to fetch last temperature: {response.get_json().get("error")}")
        return response, status_code
    except Exception as e:
        module_logger.error(f"Error fetching last temperature: {e}", exc_info=True)
        return jsonify({"error": "Failed to retrieve last temperature"}), 500

def get_temperature_by_id_service(temperature_id):
    module_logger.debug(f"Request received to fetch the temperature with id: {temperature_id}")
    try:
        response, status_code = get_temperature_by_id(temperature_id)
        if status_code == 200:
            module_logger.info(f"Successfully fetched temperature with id: {temperature_id}")
        else:
            module_logger.warning({response.get_json().get("error")})
        return response, status_code
    except Exception as e:
        module_logger.error(f"Error fetching temperature with id {temperature_id}: {e}", exc_info=True)
        return jsonify({"error": "Failed to retrieve temperature"}), 500

def delete_last_temperature_service():
    module_logger.debug("Request received to delete the last temperature record")
    try:
        response, status_code = delete_last_temperature()
        if status_code == 200:
            module_logger.info("Successfully deleted the last temperature record")
        else:
            module_logger.warning(response.get_json().get("error"))
        return response, status_code
    except Exception as e:
        module_logger.error(f"Exception occurred while deleting last temperature: {e}", exc_info=True)
        return jsonify({"error": "Failed to delete last temperature"}), 500

def delete_temperature_by_id_service(temperature_id: int):
    module_logger.debug(f"Request received to delete temperature with id: {temperature_id}")
    try:
        response, status_code = delete_temperature_by_id(temperature_id)
        if status_code == 200:
            module_logger.info(f"Successfully deleted temperature with id: {temperature_id}")
        else:
            module_logger.warning(f"Failed to delete temperature with id {temperature_id}: {response.get_json().get("error")}")
        return response, status_code
    except Exception as e:
        module_logger.error(f"Exception occurred while deleting temperature by id {temperature_id}: {e}", exc_info=True)
        return jsonify({"error": "Failed to delete temperature"}), 500

def get_all_temperatures_by_sorting_service(sort_order: str):
    module_logger.debug(f"Request received to fetch all temperatures sorted by: '{sort_order}'")
    try:
        response, status_code = get_all_temperatures_by_sorting(sort_order)
        if status_code == 200:
            module_logger.info(f"Successfully fetched all temperatures sorted '{sort_order}'")
        else:
            module_logger.warning(response.get_json().get("error"))
        return response, status_code
    except Exception as e:
        module_logger.error(f"Exception occurred while fetching sorted temperatures '{sort_order}': {e}", exc_info=True)
        return jsonify({"error": "Failed to retrieve temperatures"}), 500

def get_last_temperatures_service(limit: int):
    module_logger.debug(f"Request received to fetch last {limit} temperatures")
    try:
        response, status_code = get_last_temperatures(limit)
        if status_code == 200:
            module_logger.info(f"Successfully fetched last {limit} temperatures")
        else:
            module_logger.warning(response.get_json().get("error"))
        return response, status_code
    except Exception as e:
        module_logger.error(f"Exception occurred while fetching last {limit} temperatures: {e}", exc_info=True)
        return jsonify({"error": "Failed to retrieve temperatures"}), 500
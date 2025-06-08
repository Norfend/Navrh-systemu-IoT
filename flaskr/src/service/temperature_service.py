from repository.temperature_repository import (add_temperature, get_last_temperature, get_temperature_by_id,
                                               delete_last_temperature, delete_temperature_by_id,
                                               get_all_temperatures_by_sorting)


def add_temperature_service(temperature_value, measurement_time, sending_time):
    return add_temperature(temperature_value, measurement_time, sending_time)

def get_last_temperature_service():
    return get_last_temperature()

def get_temperature_by_id_service(temperature_id):
    return get_temperature_by_id(temperature_id)

def delete_last_temperature_service():
    return delete_last_temperature()

def delete_temperature_by_id_service(temperature_id):
    return delete_temperature_by_id(temperature_id)

def get_all_temperatures_by_sorting_service(sort_order):
    return get_all_temperatures_by_sorting(sort_order)
from datetime import datetime

from flask import jsonify

from model.Temperature import Temperature
from utils.database import db


def add_temperature(temperature_value, measurement_time, sending_time):
    measurement_date = datetime.strptime(measurement_time, "%Y-%m-%d %H:%M:%S")
    sending_date = datetime.strptime(sending_time, "%Y-%m-%d %H:%M:%S")
    new_temperature = Temperature(
        temperature=temperature_value, measurement_time=measurement_date, sending_time=sending_date
    )

    if not new_temperature:
        return jsonify({"error": "Temperature wasn't added"}), 500

    db.session.add(new_temperature)
    db.session.commit()

    return jsonify({"message": "Temperature added successfully!", "id": new_temperature.id}), 201

def get_last_temperature():
    try:
        last_record = db.session.query(Temperature).order_by(Temperature.id.desc()).first()
        if last_record:
            return jsonify(
                {
                    'temperature': last_record.temperature,
                    'receiving_timestamp': last_record.formatted_receiving_time
                }), 200
        return jsonify({"error": "Temperature wasn't founded"}), 500

    except Exception as e:
        raise e

def get_temperature_by_id(temperature_id : int):
    try:
        found_temperature = db.session.query(Temperature).filter(Temperature.id == temperature_id).first()
        if found_temperature:
            return jsonify(
                {
                    'id': found_temperature.id,
                    'temperature': found_temperature.temperature,
                    'receiving_timestamp': found_temperature.formatted_receiving_time
                }), 200
        return jsonify({"error": "Temperature wasn't founded"}), 400

    except Exception as e:
        raise e

def get_last_temperatures(limit : int):
    try:
        found_temperatures = (db.session.query(Temperature)
                              .order_by(Temperature.receiving_timestamp.desc()).limit(limit).all())
        if found_temperatures:
            serialized = [
                {
                    'temperature': temp.temperature,
                    'measurement_time': temp.formatted_measurement_time,
                    'sending_time': temp.formatted_sending_time,
                    'receiving_timestamp': temp.formatted_receiving_time
                }
                for temp in found_temperatures
            ]
            return jsonify(serialized), 200
        return jsonify({"error": "Temperatures wasn't founded"}), 400

    except Exception as e:
        raise e

def delete_last_temperature():
    try:
        last_temperature = db.session.query(Temperature).order_by(Temperature.receiving_timestamp.desc()).first()
        if last_temperature:
            db.session.delete(last_temperature)
            db.session.commit()
            return jsonify({"message": "Successfully deleted"}), 200
        return jsonify({"error": "Temperature wasn't deleted"}), 500

    except Exception as e:
        db.session.rollback()
        raise e

def delete_temperature_by_id(temperature_id : int):
    try:
        found_temperature = db.session.query(Temperature).filter(Temperature.id == temperature_id).first()
        if found_temperature:
            db.session.delete(found_temperature)
            db.session.commit()
            return jsonify({"message": "Successfully deleted"}), 200
        return jsonify({"error": "Temperature wasn't founded"}), 400

    except Exception as e:
        db.session.rollback()
        raise e

def get_all_temperatures_by_sorting(sort_order: str = 'asc'):
    try:
        if sort_order not in ['asc', 'desc']:
            return jsonify({'error': 'Invalid sort parameter. Use "asc" or "desc".'}), 400

        query = db.session.query(Temperature)
        if sort_order == 'asc':
            temperatures = query.order_by(Temperature.receiving_timestamp.asc()).all()
        else:
            temperatures = query.order_by(Temperature.receiving_timestamp.desc()).all()

        result = [{
            'id': temp.id,
            'temperature': temp.temperature,
            'receiving_timestamp': temp.formatted_receiving_time
        } for temp in temperatures]

        return jsonify(result), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred.'}), 500
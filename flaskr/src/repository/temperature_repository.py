import string

from flask import jsonify

from model.Temperature import Temperature
from utils.database import db


def add_temperature(temperature_value):
    new_temperature = Temperature(temperature=temperature_value)

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
                    'id': last_record.id,
                    'temperature': last_record.temperature,
                    'timestamp': last_record.formatted_timestamp
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
                    'timestamp': found_temperature.formatted_timestamp
                }), 200
        return jsonify({"error": "Temperature wasn't founded"}), 400

    except Exception as e:
        raise e

def get_last_temperatures(limit : int):
    try:
        found_temperatures = db.session.query(Temperature).order_by(Temperature.timestamp.desc()).limit(limit).all()
        if found_temperatures:
            serialized = [
                {
                    'id': temp.id,
                    'temperature': temp.temperature,
                    'timestamp': temp.formatted_timestamp
                }
                for temp in found_temperatures
            ]
            return jsonify(serialized), 200
        return jsonify({"error": "Temperatures wasn't founded"}), 400

    except Exception as e:
        raise e

def delete_last_temperature():
    try:
        last_temperature = db.session.query(Temperature).order_by(Temperature.timestamp.desc()).first()
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
            temperatures = query.order_by(Temperature.timestamp.asc()).all()
        else:
            temperatures = query.order_by(Temperature.timestamp.desc()).all()

        result = [{
            'id': temp.id,
            'temperature': temp.temperature,
            'timestamp': temp.formatted_timestamp
        } for temp in temperatures]

        return jsonify(result), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred.'}), 500
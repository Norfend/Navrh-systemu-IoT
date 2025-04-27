from flask import jsonify

from model.Temperature import Temperature
from utils.database import db


def add_temperature(temperature_value):
    if not temperature_value:
        return jsonify({"error": "Temperature value is required"}), 400

    new_temperature = Temperature(temperature=temperature_value)

    if not new_temperature:
        return jsonify({"error": "Temperature wasn't added"}), 500

    db.session.add(new_temperature)
    db.session.commit()

    return jsonify({"message": "Temperature added successfully!", "id": new_temperature.id}), 201

def get_last_temperature():
    try:
        last_record = (db.session.query(Temperature).order_by(Temperature.timestamp.desc()).first())
        if last_record:
            return {
                'temperature': last_record.temperature,
                'timestamp': last_record.formatted_timestamp
            }
        return None

    except Exception as e:
        db.session.rollback()
        raise e
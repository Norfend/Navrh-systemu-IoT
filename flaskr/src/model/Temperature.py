from datetime import datetime, timezone, timedelta

from utils.database import db


def get_timestamp():
    return datetime.now(tz=timezone(timedelta(hours=2)))

class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    measurement_time = db.Column(db.DateTime, nullable=False)
    sending_time = db.Column(db.DateTime, nullable=False)
    receiving_timestamp = db.Column(db.DateTime, default=get_timestamp)

    @property
    def formatted_measurement_time(self):
        return self.measurement_time.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def formatted_sending_time(self):
        return self.sending_time.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def formatted_receiving_time(self):
        return self.receiving_timestamp.strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return f"<Temperature {self.temperature}°C at {self.timestamp}>"
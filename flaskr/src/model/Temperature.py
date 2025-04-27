from datetime import datetime, timezone, timedelta

from utils.database import db


def get_timestamp():
    return datetime.now(tz=timezone(timedelta(hours=2)))

class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=get_timestamp)

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return f"<Temperature {self.temperature}°C at {self.timestamp}>"
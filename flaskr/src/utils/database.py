import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()
module_logger = logging.getLogger(__name__)

def check_database():
    try:
        db.session.execute(text('SELECT 1'))
        return True
    except Exception as e:
        return False
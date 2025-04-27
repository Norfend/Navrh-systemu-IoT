from controller.api_routes import temperature_routes
from controller.routes import all_routes

def setup_routes(app, db):
    with app.app_context():
        db.create_all()

    all_routes(app)
    temperature_routes(app)
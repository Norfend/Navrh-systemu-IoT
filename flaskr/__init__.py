from flask import Flask
import routes
from DataStore import DataStore

def create_app():
    application = Flask(__name__)
    application.data_store = DataStore()

    from routes import bp
    application.register_blueprint(bp)

    return application

if __name__ == "__main__":
    app = create_app()
    app.run()
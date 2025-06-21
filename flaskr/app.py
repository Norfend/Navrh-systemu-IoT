from waitress import serve
from utils.factory import create_app

app = create_app()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5001, _quiet=False, url_scheme='https')
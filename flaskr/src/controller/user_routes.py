from flask_login import login_required

from service.user_service import login_service, register_service, logout_service


def user_routes(app):
    @app.route("/login", methods=["GET", "POST"])
    def login_controller():
        return login_service()

    @app.route("/register", methods=["GET", "POST"])
    def register_controller():
        return register_service()

    @login_required
    @app.route('/logout', methods=["POST"])
    def logout_controller():
        return logout_service()
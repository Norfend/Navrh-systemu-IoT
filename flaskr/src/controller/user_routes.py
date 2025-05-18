from flask_login import login_required

from repository.user_repository import login, logout, register

def user_routes(app):
    @app.route("/login", methods=["GET", "POST"])
    def login_controller():
        return login()

    @app.route("/register", methods=["GET", "POST"])
    def register_controller():
        return register()

    @login_required
    @app.route('/logout', methods=["POST"])
    def logout_controller():
        return logout()
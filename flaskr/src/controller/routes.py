from service.dashboard import dashboard, delete_oldest, update_table
from service.user import login, logout, register

from model.temperature_data import Temperature
from model.users_data import User

data_base = Temperature()
user_base = User()

def all_routes(app):
    @app.route("/dashboard", methods=["GET"])
    def dashboard_controller():
        return dashboard(data_base)

    @app.route("/update_table", methods=["GET"])
    def update_table_controller():
        return update_table(data_base)

    @app.route("/delete_oldest", methods=["POST"])
    def delete_oldest_controller():
        return delete_oldest(data_base)

    @app.route("/login", methods=["GET", "POST"])
    def login_controller():
        return login(user_base)

    @app.route('/logout', methods=["POST"])
    def logout_controller():
        return logout()

    @app.route("/register", methods=["GET", "POST"])
    def register_controller():
        return register(user_base)
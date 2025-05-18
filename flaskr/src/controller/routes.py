from flask_login import login_required

from service.dashboard import dashboard, update_table


def all_routes(app):
    @app.route("/dashboard", methods=["GET"])
    @login_required
    def dashboard_controller():
        return dashboard()

    @app.route("/update_table", methods=["GET"])
    @login_required
    def update_table_controller():
        return update_table()
from flask import Blueprint, render_template, redirect, url_for
from flask import current_app

bp = Blueprint('dashboard', __name__)

@bp.route("/")
def dashboard():
    data = current_app.data_store
    latest = data.get_latest()
    last_15 = data.get_last_15()

    return render_template("dashboard.html", latest=latest, measurements=last_15)


@bp.route("/delete_oldest", methods=["POST"])
def delete_oldest():
    current_app.data_store.delete_oldest()
    return redirect(url_for('dashboard.dashboard'))
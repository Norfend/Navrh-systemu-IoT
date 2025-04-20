from flask import render_template, request, redirect, url_for, session
from data.temperature_data import Data
from data.users_data import User

def setup_routes(app):
    data_base = Data()
    user_base = User()

    @app.route("/dashboard", methods=["GET"])
    def dashboard():
        if 'username' not in session:
            return redirect(url_for('login'))

        latest = data_base.get_latest()
        last_15 = data_base.get_last_15()

        return render_template("dashboard.html", latest=latest, measurements=last_15)

    @app.route("/delete_oldest", methods=["POST"])
    def delete_oldest():
        data_base.delete_oldest()

        return redirect(url_for("dashboard"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            database_password = user_base.get_user_password(username)
            if database_password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                return "Invalid credentials, please try again."

        return render_template("login.html")

    # @app.route("/register", methods=["GET", "POST"])
    # def register():
    #     if request.method == "POST":
    #         username = request.form.get("username")
    #         password = request.form.get("password")
    #
    #         if username in users:
    #             return "Username already exists, try another one."
    #
    #         users[username] = password
    #         return redirect(url_for('login'))
    #
    #     return render_template("register.html")

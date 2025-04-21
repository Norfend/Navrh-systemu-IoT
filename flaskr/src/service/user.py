from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash


def login(user_base):
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        hashed = user_base.get_user_password(username)

        if check_password_hash(hashed, password):
            session['username'] = username
            flash("✅ Successfully logged in!", "success")
            return redirect(url_for('dashboard_controller'))
        else:
            flash("⚠ Invalid credentials, please try again.", "danger")
            return redirect(url_for('login_controller'))

    return render_template("login.html")

def logout():
    session.clear()
    return redirect(url_for('login_controller'))

def register(user_base):
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        registered = user_base.add_user(username, password)
        if not registered:
            flash("⚠ Username already exists, try another one.", "danger")
            return redirect(url_for('register_controller'))

        flash("✅ Registration successful! You can now log in.", "success")
        return redirect(url_for('login_controller'))

    return render_template("register.html")
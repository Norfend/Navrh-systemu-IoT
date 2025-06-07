from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from model.User import User
from utils.database import db


def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(login=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("✅ Successfully logged in!", "success")
            return redirect(url_for('dashboard_controller'))
        else:
            flash("⚠ Invalid credentials, please try again.", "danger")
            return redirect(url_for('login_controller'))

    return render_template("login.html")

def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)

        new_user = User(login=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()
            flash("⚠ Username already exists, try another one.", "danger")
            return redirect(url_for('register_controller'))
        else:
            db.session.commit()
            flash("✅ Registration successful! You can now log in.", "success")
            return redirect(url_for('login_controller'))
    return render_template("register.html")

def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login_controller'))
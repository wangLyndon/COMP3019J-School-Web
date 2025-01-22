import logging

import requests
from flask import redirect, url_for, flash, render_template, request, jsonify, current_app
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User, Student, Teacher, RestaurantStaff


@bp.route("/login", methods=["GET", "POST"])
def login():
    # The logged in user returns to the home page directly
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()

        if not user:
            flash('No user found with username: {}'.format(form.username.data))
            return redirect(url_for("auth.login"))
        if not (check_password_hash(user.passwordHash, form.password.data)):
            flash("Wrong username or password")
            return redirect(url_for("auth.login"))

        if user.ban == "Ban":
            logging.getLogger("login").info(f"{user.username} want to login, which is banned")

            return redirect(url_for("main.banPage"))

        login_user(user, remember=form.remember_me.data)

        logging.getLogger("login").info(f"{user.username} login to the web")

        return redirect(url_for("main.index"))
    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        checkName = User.query.filter(User.username == form.username.data).first()
        if checkName:
            flash("This name is already register, change it")
            return redirect(url_for("auth.register"))

        checkEmail = User.query.filter(User.email == form.email.data).first()
        if checkEmail:
            flash("This email is already register, change it")
            return redirect(url_for("auth.register"))

        checkPhone = User.query.filter(User.phoneNumber == form.phoneNumber.data).first()
        if checkPhone:
            flash("This phone number is already register, change it")
            return redirect(url_for("auth.register"))

        passwordHash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, passwordHash=passwordHash, email=form.email.data, role=form.role.data,
                    phoneNumber=form.phoneNumber.data, address=form.address.data)
        db.session.add(user)
        db.session.commit()

        if user.role == "student":
            student = Student(userId=user.id)
            db.session.add(student)
        elif user.role == "teacher":
            teacher = Teacher(userId=user.id)
            db.session.add(teacher)
        elif user.role == "restaurantStaff":
            staff = RestaurantStaff(userId=user.id)
            db.session.add(staff)
        db.session.commit()

        flash("Successful registration")

        logging.getLogger("register").info(f"{user.username} register to the web")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@bp.route("/chat", methods=["POST"])
def chat():
    # Make sure other routes can also use chat

    message = request.get_json().get("message")

    headers = {
        "Content-Type": "application/json"
    }

    requestOptions = {
        "message": message
    }

    result = requests.post("http://localhost:5000/chat", headers=headers, json=requestOptions)

    return jsonify(result.json())


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))

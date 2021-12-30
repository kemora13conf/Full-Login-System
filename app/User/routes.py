from flask import render_template, flash, redirect, url_for, request, jsonify, json
from . import users
from .forms import RegistrationForm, LoginForm, ResetReqForm, ResetPasswordForm
from ..Models import Users
from .. import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from .utils import crop_pic, send_reset_email

"""
    This file contain all the route for the login and the registration routes
"""


@users.route('/Registration', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        picture = crop_pic(form.picture.data)
        user = Users(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=hash_pwd, picture=picture)
        db.session.add(user)
        db.session.commit()
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user)
            flash('Account created succesfully!',category='Succes')
            return redirect(url_for('main.home'))
        flash('Something went wrong!', category="Warning")
        return redirect(url_for('users.register'))
    return render_template('User/Register.html', title="Registration",
                            form=form)

@users.route('/Login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    #flash('Welcome To Your Account!',category='Succes')
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Welcome To Your Account!',category='Succes')
                data = request.args.get('next')
                return redirect(data) if data else redirect(url_for('main.home'))
            else:
                flash('Wrong password, Try again!', category='Warning')
        else:
            flash('Wrong email, Try again!', category='Warning')
        return redirect(url_for('users.login'))
    return render_template('User/Login.html', title="Login",
                            form=form)

@users.route('/Reset-Password', methods=['GET','POST'])
def reset_req():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetReqForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instraction to reset your password.', category='Succes')
        return redirect(url_for('users.login'))
    return render_template('User/ResetReq.html', title="Reset-Password", form=form)

@users.route('/Reset-Password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = Users.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', category='Wrong')
        return redirect(url_for('users.reset_req'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = password_hash 
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('User/PasswordUpdate.html', title="Reset-Password", form=form)

@users.route('/Logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))




# This used to check if the user's info
@users.route('/API/Check_info/<type>/<data>')
def check_user(type, data):
    if type == "email":
        user = Users.query.filter_by(email=data).first()
        if user:
            return jsonify("Yes")
    elif type == "username":
        user = Users.query.filter_by(username=data).first()
        if user:
            return jsonify("Yes")
    else:
        return jsonify("No")
    return redirect(url_for('users.login'))
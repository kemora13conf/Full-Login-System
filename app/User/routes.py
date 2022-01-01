from flask import render_template, flash, redirect, url_for, request, jsonify, json
from . import users
from .forms import Reg_1_Form, Reg_2_Form, Reg_3_Form, LoginForm, ResetReqForm, ResetPasswordForm
from ..Models import Users
from .. import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from .utils import crop_pic, send_reset_email

"""
    This file contain all the route for the login and the registration routes
"""


# The registration views

@users.route('/Registration-Part-1', methods=['GET','POST'])
def reg_1():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = Reg_1_Form()
    if form.validate_on_submit():
        userInfo = {
            'firstname': form.firstname.data,
            'lastname': form.lastname.data,
            'username': form.username.data
        }

        return redirect(url_for('users.reg_2', userInfo=json.dumps(userInfo)))
    return render_template('User/Reg_1.html', title="Registration",
                            form=form)

@users.route('/Registration-Part-2/<userInfo>', methods=['GET','POST'])
def reg_2(userInfo):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    userInfo = json.loads(userInfo)
    form=Reg_2_Form()
    if form.validate_on_submit():

        userInfo['email'] = form.email.data
        userInfo['password'] = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        return redirect(url_for('users.reg_3', userInfo=json.dumps(userInfo)))
    return render_template('User/Reg_2.html', title="Registration",
                            form=form)
@users.route('/Registration-Part-3/<userInfo>', methods=['GET','POST'])
def reg_3(userInfo):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    userInfo = json.loads(userInfo)
    form=Reg_3_Form()
    if form.validate_on_submit():
        
        picture = crop_pic(form.picture.data)
        user = Users(firstname=userInfo['firstname'], lastname=userInfo['lastname'], username=userInfo['username'], email=userInfo['email'], password=userInfo['password'], picture=picture)
        db.session.add(user)
        db.session.commit()
        userInfo.clear()
        user = Users.query.filter_by(username=userInfo['username']).first()
        if user:
            login_user(user)
            flash('Account created succesfully!',category='Succes')
            return redirect(url_for('main.home'))
        flash('Something went wrong!', category="Warning")
        return redirect(url_for('users.reg_1'))
    return render_template('User/Reg_3.html', title="Registration",
                            form=form)

# The login and the password reset views
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